#!/bin/sh
# include support for sphinx configs
# until real include directive added, which may be never
# http://sphinxsearch.com/bugs/view.php?id=964

dir=$(dirname "$0")

# load global config: indexer, searchd
cat $dir/sphinx-common.conf

# load extra indexes definitons
for config in $dir/index.d/*.conf; do
	if [ -f "$config" ]; then
		cat "$config"
	fi
done
