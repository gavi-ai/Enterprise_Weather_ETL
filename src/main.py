import subprocess
import time
import sys

print("🚀 [ENTERPRISE PIPELINE]: Initializing the Master Orchestrator...")
print("=================================================================")

pipeline_stages = [
    {"name": "Extract (Bronze Layer)", "script": "src/data_generator.py"},
    {"name": "Transform & Enrich (Silver Layer)", "script": "src/transform_silver.py"},
    {"name": "Business Aggregation (Gold Layer)", "script": "src/transform_gold.py"}
]

total_start_time = time.time()
pipeline_success = True # The God-Switch

for stage in pipeline_stages:
    print(f"\n⏳ [RUNNING]: {stage['name']}...")
    stage_start = time.time()
    
    try:
        result = subprocess.run(["python3", stage["script"]], check=True, text=True, capture_output=True)
        print(result.stdout) 
        
        stage_end = time.time()
        print(f"✅ [COMPLETED]: {stage['name']} in {round(stage_end - stage_start, 2)} seconds.")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ [CRITICAL PIPELINE FAILURE]: {stage['name']} crashed!")
        print(f"Error Details: {e.stderr}")
        print("🛑 [SYSTEM]: Halting pipeline to prevent bad data.")
        pipeline_success = False # Switch flipped to failure
        break 

total_end_time = time.time()
print("\n=================================================================")

# The Corporate Logic: Sirf tabhi celebrate karo jab sach mein success ho
if pipeline_success:
    print(f"🎉 [SUCCESS]: Entire Enterprise Pipeline executed successfully in {round(total_end_time - total_start_time, 2)} seconds!")
    print("💳 [MAALKIN ALERT]: Ishika's weather & revenue dashboards are officially updated and ready to print money.")
else:
    print("☠️ [FAILURE]: Pipeline aborted. Maalkin's card is temporarily blocked until bugs are fixed!")
    sys.exit(1) # Hard crash the system