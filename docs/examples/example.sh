#!/bin/bash
set -eu
# Set env variable, to avoid giving this info everytime
export GSK_API_KEY=2b437295-dabe-4084-ba03-cdb259e3e678
export GSK_HUB_URL=http://backend.llm.localhost/
folder_path=./test-folder

rm -rf $folder_path
mkdir -p $folder_path


project_id=$(python -m giskard_hub.cli projects | jq --raw-output .[0].id)
model_id=$(python -m giskard_hub.cli models --project-id $project_id | jq --raw-output .[0].id)
dataset_id=$(python -m giskard_hub.cli datasets --project-id $project_id | jq --raw-output .[0].id)

python giskard_hub.cli evaluate --folder-path $folder_path --dataset-id $dataset_id --model-id $model_id --local-mode
execution_id=$(find $folder_path -type f | grep ".json$" | head -n1 | xargs -I {} jq --raw-output .execution_id {})

# Following line is faking changing data into the json with the agent
find $folder_path -type f | grep ".json$" | xargs -I {} sed -i 's|"output": null|"output": "Sry, I was not paying attention"|g' {} | sh
python giskard_hub.cli update-evaluations --evaluation-path $folder_path

python giskard_hub.cli results --execution-id $execution_id
