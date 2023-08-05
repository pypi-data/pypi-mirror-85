#!/usr/bin/env bash


# remove the git index
#[ -f .git/index ] && rm .git/index || true

#rm -rf dist *egg-info || true

find ./ -name '__pycache__' -exec rm -rf {} \; || true


set nounset
set errexit

function replace {
    from=$1
    to=$2

    for d in `find ./ -depth -type d`
    do
        new=`echo $d | sed "s/$from/$to/g"`
        [ "$d" != "$new" ] && mv $d $new
    done

    for f in `find ./ -type f`
    do
        new=`echo $f | sed "s/$from/$to/g"`
        [ "$f" != "$new" ] && mv $f $new
    done

    for f in `find ./ -type f -not -name '.git' -not -name 'rename_plugin.sh'`
    do
        sed -i "s/$from/$to/g" $f
    done

}



## RENAME THE PLUGIN
replace "_index_blueprint" "_chunked_index"
replace "-index-blueprint" "-chunked-index"

replace "IndexBlueprint" "ChunkedIndex"
replace "indexBlueprint" "chunkedIndex"

replace "_INDEX_BLUEPRINT" "_CHUNKED_INDEX"
replace "-INDEX-BLUEPRINT" "-CHUNKED-INDEX"


# RENAME THE INDEX CLASSES
replace "_item"  "_chunked"
replace "-item" "-chunked"

replace "_ITEM" "_CHUNKED"
replace "-ITEM" "-CHUNKED"

replace "Item" "Chunked"
replace "item" "chunked"



# Remove compile generated javascript
find ./ -type f -not -name '.git' -name "*.js" -exec rm {} \; || true
find ./ -type f -not -name '.git' -name "*.js.map" -exec rm {} \; || true
