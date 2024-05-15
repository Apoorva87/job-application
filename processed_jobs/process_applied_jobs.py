import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def update_applied_status(data, job_ids):
    for job in data:
        if job.get('id') in job_ids:
            job['applied'] = True
    return data

def main():
    file_path = 'WFScrapper_processed.json'  # Use the same path for input and output

    #input_file = 'WFScrapper_processed.json'
    #output_file = 'WFScrapper_processed_applied.json'

    # Load existing data
    data = load_json(file_path)
    #data = load_json(input_file)

    # Get job IDs from the user
    job_ids = input("Enter the job IDs separated by commas: ").split(',')

    # Strip any extra whitespace from the job IDs
    job_ids = [job_id.strip() for job_id in job_ids]

    # Update the applied status
    updated_data = update_applied_status(data, job_ids)

    # Save the updated data
    save_json(updated_data, file_path)
    print(f"Updated data saved to {file_path}")

if __name__ == "__main__":
    main()
