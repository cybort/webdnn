# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = MILWebDNN
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile ts

ts:
	rm -rf build/html/api_reference/descriptor-runner
	$(shell npm bin)/typedoc \
		--out build/html/api_reference/descriptor-runner \
		--mode file \
		--target es2017 \
		--lib "lib.es2017.d.ts,lib.dom.d.ts" \
		--excludePrivate \
		--readme source/api_reference/descriptor-runner/index.md \
		../src/descriptor_runner

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	$(MAKE) ts
