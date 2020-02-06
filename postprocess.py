import re
import os
import time
import json
import argparse
import subprocess
from pathlib import Path


_re_multi_space = re.compile(r"\s+")
_re_return = re.compile(r"\n")
_re_bold = re.compile(r"\*\*([^\*]+)\*\*")
_re_ital = re.compile(r"\_([^\_]+)\_")
_re_ref = re.compile(r"\[\d+\]")
_re_img = re.compile(r"\*\[\!\[[^\[]+\]\([^\(]+\)\]\:")
_re_start_bracket = re.compile(r"\*\[[^\[]+\]\:")
_re_bracket = re.compile(r"\([^\(]+\)")

_re_json_content = re.compile(r'"content"\s*:\s*"(.+)"\}')

def regex_process(text):
    text = re.sub(_re_return, "", text)
    text = re.sub(_re_multi_space, " ", text)
    text = re.sub(_re_bold, lambda match: match.group(1), text)
    text = re.sub(_re_ital, lambda match: match.group(1), text)
    text = re.sub(_re_ref, "", text)
    text = re.sub(_re_img, "", text) # img should before start bracket
    text = re.sub(_re_start_bracket, "", text)
    text = re.sub(_re_bracket, "", text)
    return text

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--indir", required=True)

    parser.add_argument("--outdir", required=True)

    parser.add_argument("--file_size", default=100000)

    args = parser.parse_args()

    json_files = [path for path in Path(args.indir).iterdir() if path.name.endswith(".json")]

    os.makedirs(args.outdir, exist_ok=True)

    res = subprocess.run(f"wc -l {args.indir}/*", shell=True, stdout=subprocess.PIPE)

    total_lines = int(re.findall(r"(\d+) ", res.stdout.decode("utf-8") )[-1])

    print(f"total lines: {total_lines}")

    write_file_idx = 0
    write_line_idx = 0
    write_lines_per_file = int(args.file_size)

    fw = open(Path(f"{args.outdir}") / f"out_{write_file_idx:06d}.txt", "w")

    idx = 0
    idx_show = 0
    idx_show_total = 100
    t0 = time.time()
    for json_file in json_files:
        print(f"process file: {json_file}")

        with open(json_file, 'r') as f:

            while True:

                if idx % (total_lines // idx_show_total) == 0:
                    print(f"progress [{idx_show}%] time {time.time()-t0:.2f}")
                    idx_show += 1

                idx += 1

                if idx == 11:
                    a = 1

                line = f.readline()

                if line == "":
                    break

                # content_list = re.findall(_re_json_content, line)

                # if len(content_list) == 1:
                #     content = regex_process(content_list[0])
                #
                #     if not re.match(".*[a-zA-Z].*", content):
                #         continue
                #
                # else:
                #     continue

                if line.strip().endswith(","):
                    try:
                        d = json.loads(line.strip())
                        content = d['content']

                    except Exception as e:
                        continue

                    content = regex_process(content)

                    if not re.match(".*[a-zA-Z].*", content):
                        continue

                else:
                    continue


                fw.write(content.strip() + "\n")
                # fw.flush()
                write_line_idx += 1

                if write_line_idx == write_lines_per_file:
                    fw.close()
                    write_line_idx = 0
                    write_file_idx += 1
                    fw = open(Path(f"{args.outdir}") / f"out_{write_file_idx:06d}.txt", "w")
