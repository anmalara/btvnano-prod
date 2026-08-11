#!/usr/bin/env bash

download_sample() {
    local dataset_file="$1"
    local dataset_line="$2"
    local mini_name="$3"
    local central_name="$4"
    local dasgoclient="/cvmfs/cms.cern.ch/common/dasgoclient"

    local dataset
    dataset=$(sed -n "${dataset_line}p" "$dataset_file")
    if [[ -z "$dataset" ]]; then
        echo "Dataset entry not found: $dataset_file line $dataset_line" >&2
        return 1
    fi
    echo "Dataset: $dataset" >&2

    local mini_file
    mini_file=$("$dasgoclient" -query="file dataset=$dataset" | head -n 1)
    if [[ -z "$mini_file" ]]; then
        echo "No MiniAOD file found for $dataset" >&2
        return 1
    fi
    echo "MiniAOD: $mini_file" >&2

    local central_file
    central_file=$("$dasgoclient" -query="child file=$mini_file" | grep NANOAOD | head -n 1)
    if [[ -z "$central_file" ]]; then
        echo "No NanoAOD daughter found for $mini_file" >&2
        return 1
    fi
    echo "NanoAOD: $central_file" >&2

    if [[ -e "$mini_name" || -e "$central_name" ]]; then
        echo "Refusing to overwrite $mini_name or $central_name; remove them first." >&2
        return 1
    fi

    xrdcp "root://cms-xrd-global.cern.ch/$mini_file" "$mini_name" >&2 || return 1
    xrdcp "root://cms-xrd-global.cern.ch/$central_file" "$central_name" >&2 || return 1
    printf '%s %s\n' "$mini_name" "$central_name"
}

run_pfnano() {
    local config_path="$1"
    local input_file="$2"
    local output_file="$3"

    local source_dir
    source_dir=$(pwd)
    local tmp_root="${TMPDIR:-/tmp}/${USER:-$(id -un)}"
    mkdir -p "$tmp_root" || return 1
    local tmpdir
    tmpdir=$(mktemp -d "$tmp_root/test_local.XXXXXX") || return 1

    local config_input
    config_input=$(sed -n 's/.*file:\([^" ]*\).*/\1/p' "$config_path" | head -n 1)
    local config_output
    config_output=$(sed -n 's/.*fileName=cms.untracked.string("\([^"]*_NANO.root\)").*/\1/p' "$config_path" | head -n 1)
    local histogram_file="${output_file%_PFNANO.root}_histograms.root"

    cp utils/ScriptExe.sh utils/mergeHistogramInFile.py "$tmpdir/"
    chmod +x "$tmpdir/ScriptExe.sh"
    cp "$config_path" "$tmpdir/PSet.py"
    sed -i 's/input=cms.untracked.int32(-1)/input=cms.untracked.int32(10000)/' \
        "$tmpdir/PSet.py"
    ln -s "$source_dir/$input_file" "$tmpdir/$config_input"

    (
        cd "$tmpdir" || exit 1
        ./ScriptExe.sh
    ) || return 1

    cp "$tmpdir/$config_output" "$source_dir/$output_file" || return 1
    if [[ -f "$tmpdir/histograms.root" ]]; then
        cp "$tmpdir/histograms.root" "$source_dir/$histogram_file" || return 1
    fi
    rm -rf "$tmpdir"
}

compare_nano() {
    local pfnano_file="$1"
    local central_file="$2"

    python3 utils/compare_root_files.py \
        --pfnano "$pfnano_file" \
        --nano "$central_file" \
        --max-events 10000
}

test_local() {
    if [[ $# -ne 2 ]]; then
        echo "Usage: test_local mc|data year" >&2
        return 2
    fi

    local type="$1"
    local year="$2"
    local dataset_file
    local dataset_line
    local config_path
    local mini_name
    local central_name
    local pfnano_name

    case "$type:$year" in
        mc:2024)
            dataset_file="datasets/mc_2024_QCD_Znunu.txt"
            dataset_line=4
            config_path="utils/mc_2024_NANO.py"
            mini_name="mc_2024_PTNuNu600_PAT.root"
            central_name="mc_2024_PTNuNu600_CENTRAL.root"
            pfnano_name="mc_2024_PTNuNu600_PFNANO.root"
            ;;
        mc:2022)
            dataset_file="datasets/mc_2022_EWK_Znunu.txt"
            dataset_line=1
            config_path="utils/mc_2022_NANO.py"
            mini_name="mc_2022_VBFto2Nu_PAT.root"
            central_name="mc_2022_VBFto2Nu_CENTRAL.root"
            pfnano_name="mc_2022_VBFto2Nu_PFNANO.root"
            ;;
        data:24|data:2024)
            dataset_file="datasets/data_2024.txt"
            dataset_line=1
            config_path="utils/data_2024_NANO.py"
            mini_name="data_2024_Run2024C_PAT.root"
            central_name="data_2024_Run2024C_CENTRAL.root"
            pfnano_name="data_2024_Run2024C_PFNANO.root"
            ;;
        *)
            echo "Unsupported test: $type $year" >&2
            return 2
            ;;
    esac

    local sample_files
    sample_files=$(download_sample "$dataset_file" "$dataset_line" "$mini_name" "$central_name") || return 1
    read -r mini_name central_name <<< "$sample_files"

    run_pfnano "$config_path" "$mini_name" "$pfnano_name" || return 1
    compare_nano "$pfnano_name" "$central_name"
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    test_local "$@"
fi
