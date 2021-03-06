from typing import List

from webdnn.backend.code_generator.allocator import MemoryLayout
from webdnn.backend.code_generator.injectors.buffer_injector import BufferInjector
from webdnn.backend.code_generator.injectors.kernel_name_injector import KernelNameInjector
from webdnn.backend.webgpu.generator import WebGPUDescriptorGenerator
from webdnn.backend.webgpu.kernel import Kernel, GPUSize
from webdnn.graph.operators.reshape import Reshape
from webdnn.util.misc import mul

template = """
kernel void %%FUNC_NAME%%(device float * %%STATIC_BUFFER%%[[buffer(0)]],
                          device float * %%DYNAMIC_BUFFER%%[[buffer(1)]],
                          const device int * %%META_BUFFER%% [[buffer(2)]],
                          uint index[[thread_position_in_grid]],
                          uint num_threads[[threads_per_grid]])
{
    const device float *x = %%LOAD_BUFFER(reshape_x)%%;
    device float *y = %%LOAD_BUFFER(reshape_y)%%;

    const int N = %%LOAD_BUFFER(reshape_N)%%;

    for (int gid = index; gid < N; gid += num_threads) {
        y[gid] = x[gid];
    }
}
"""


@WebGPUDescriptorGenerator.register_handler(Reshape)
def reshape(op: Reshape,
            memory_layout: MemoryLayout) -> List[Kernel]:
    x = memory_layout[op.inputs["x"]]
    y = memory_layout[op.outputs["y"]]

    if x.offset == y.offset:
        # Inplace
        return []

    assert x.variable.order == op.parameters["in_order"]
    assert y.variable.order == op.parameters["out_order"]
    assert y.variable.size == mul(op.parameters["out_shape"])

    buffer_injector = BufferInjector()
    buffer_injector.register({
        "reshape_x": x,
        "reshape_y": y,
        "reshape_N": y.variable.size,
    })

    name_injector = KernelNameInjector(op)

    source = template
    source = buffer_injector.inject(source)
    source = name_injector.inject(source)

    kernel = Kernel(
        {name_injector.name: source},
        name_injector.name,
        GPUSize(8, 1, 1),
        GPUSize(1024, 1, 1),
        buffer_injector.buffer,
        buffer_injector.unresolved_value_list
    )

    return [kernel]
