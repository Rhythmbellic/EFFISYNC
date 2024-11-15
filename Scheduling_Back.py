import pandas as pd
import os

class Job:
    def __init__(self, brand, product, profit, quantity, time, machines, raw_products, labor, storage, energy, wait_time=0):
        self.brand = brand
        self.product = product
        self.profit = profit
        self.quantity = quantity
        self.time = time
        self.machines = machines  # List [m1, m2, m3]
        self.raw_products = raw_products  # List [r1, r2, r3]
        self.labor = labor
        self.storage = storage
        self.energy = energy
        self.priority = 0
        self.job_order = 0
        self.wait_time = wait_time  # Use initial wait time if provided

    def calculate_priority(self):
        total_resources = self.time + sum(self.machines) + sum(self.raw_products) + self.labor + self.storage + self.energy
        adjusted_profit = (self.profit / total_resources) * self.quantity
        self.priority = adjusted_profit / total_resources

def schedule_jobs(job_input_csv, job_resource_csv, change_state_csv, output_csv="scheduled_jobs_output.csv"):
    # Read input CSVs
    job_input_df = pd.read_csv(job_input_csv, encoding='cp1252')
    job_resource_df = pd.read_csv(job_resource_csv, encoding='cp1252')
    change_state_df = pd.read_csv(change_state_csv, encoding='cp1252')
    
    change_state = change_state_df.iloc[0, 0]

    # Merge data on brand and product columns
    jobs_df = pd.merge(job_input_df, job_resource_df, on=['brand', 'product'])

    # Load previous output if it exists and create a dictionary of previous wait times
    previous_wait_times = {}
    if os.path.exists(output_csv):
        previous_output = pd.read_csv(output_csv)
        for _, row in previous_output.iterrows():
            previous_wait_times[(row['Brand'], row['Product'])] = row['Wait Time']

    # Initialize Job objects, using previous wait times if available
    jobs = []
    for _, row in jobs_df.iterrows():
        machines = [row['m1'], row['m2'], row['m3']]
        raw_products = [row['r1'], row['r2'], row['r3']]
        wait_time = previous_wait_times.get((row['brand'], row['product']), 0)
        job = Job(row['brand'], row['product'], row['profit'], row['quantity'],
                  row['time'], machines, raw_products, row['labour'], row['storage'], row['energy'], wait_time)
        job.calculate_priority()
        jobs.append(job)

    # Sort jobs by priority and then by wait time
    jobs.sort(key=lambda job: (-job.priority, job.wait_time))

    # Set job_order based on sorted priority
    for i, job in enumerate(jobs):
        job.job_order = i

    # Update wait times if change_state is 1
    if change_state == 1:
        # Increment wait times for retained jobs
        for job in jobs:
            if (job.brand, job.product) in previous_wait_times and job.job_order > 0:
                job.wait_time += 1

    # Re-sort jobs to prioritize those with wait_time > 3
    def sort_with_wait_priority():
        jobs.sort(key=lambda job: (-1 if job.wait_time > 7 else 0, -job.priority, job.job_order))
    
    sort_with_wait_priority()

    # Collect final job information
    ordered_jobs = [(job.brand, job.product, job.profit, job.quantity, job.priority, job.wait_time, job.job_order)
                    for job in jobs]

    # Save the updated job order to the output CSV
    scheduled_jobs_df = pd.DataFrame(ordered_jobs, columns=['Brand', 'Product', 'Profit', 'Quantity', 'Priority', 'Wait Time', 'Job Order'])
    scheduled_jobs_df.to_csv(output_csv, index=False)

    return scheduled_jobs_df

# Example usage
job_input_csv = r"Job_list.csv"
job_resource_csv = r"job_resources.csv"
change_state_csv = r"change_state.csv"

scheduled_jobs_df = schedule_jobs(job_input_csv, job_resource_csv, change_state_csv)


def change_state(operation):
    
    # Read the CSV file
    df = pd.read_csv('change_state.csv')
    
    # Change State acc to operation 
    if operation ==  'ADD':
        df['change_state'] = df['change_state'].replace(1,0)
    elif operation == 'Delete':
        df['change_state'] = df['change_state'].replace(0,1)

    # Save the updated file
    df.to_csv('change_state.csv', index=False)


