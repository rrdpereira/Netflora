# batch_detection.py
import subprocess
from tqdm import tqdm

def runBatchDetection(
                    thresholds=[0.01, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50],
                    # thresholds=[0.01, 0.05, 0.10],
                    detect_script_path='detect.py',
                    weights_path='weights/PALMEIRAS_Embrapa00.pt',
                    img_size=640,
                    source_path='processing/selected_images',
                    device=0,
                    save_txt=False):

    for conf in tqdm(thresholds, desc="Processing thresholds"):
        result_name = f'{conf:.2f}'  # Format the threshold as a string with 2 decimal places
        command = f'python {detect_script_path} --device {device} --weights {weights_path} --img {img_size} --conf {conf:.2f} --source {source_path} --name {result_name} --save-txt {save_txt}'  # Explicitly pass the threshold formatted with 2 decimal places
        subprocess.run(command, shell=True)
    
    print("Threshold Samples OK.")
    return

def runDetection(detect_script_path='detect.py',
                weights_path='weights/PALMEIRAS_Embrapa00.pt',
                img_size=640,
                device=0,
                save_txt=False):
        
        command = f'python {detect_script_path} --device {device} --weights {weights_path} --img {img_size} --save-txt {save_txt}'
        subprocess.run(command, shell=True)
    
        print("Detection OK.")
        return

if __name__ == '__main__':
    runDetection(weights_path='weights/PALMEIRAS_Embrapa00.pt', img_size=1536, device=0)
    runBatchDetection(weights_path='weights/PALMEIRAS_Embrapa00.pt', img_size=1536, device=0)