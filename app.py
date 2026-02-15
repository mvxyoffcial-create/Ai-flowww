import os
import io
import base64
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import torch
import numpy as np
from PIL import Image
import cv2
from diffusers import StableDiffusionInstructPix2PixPipeline, DPMSolverMultistepScheduler
from diffusers.utils import load_image
import tempfile
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

# Global variables for models
pipe = None
device = "cuda" if torch.cuda.is_available() else "cpu"

def initialize_models():
    """Initialize AI models"""
    global pipe
    
    print(f"🚀 Initializing models on {device}...")
    
    try:
        # Use InstructPix2Pix for image-to-image generation
        model_id = "timbrooks/instruct-pix2pix"
        pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            safety_checker=None
        )
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        pipe = pipe.to(device)
        
        # Enable memory optimizations
        if device == "cuda":
            pipe.enable_attention_slicing()
            pipe.enable_vae_slicing()
        
        print("✅ Models loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        print("⚠️ Running in demo mode with basic interpolation")
        return False

def interpolate_frames(image1, image2, num_frames=16):
    """Basic frame interpolation between two images"""
    frames = []
    
    # Convert PIL to numpy
    img1 = np.array(image1)
    img2 = np.array(image2)
    
    # Ensure same size
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    
    # Generate interpolated frames
    for i in range(num_frames):
        alpha = i / (num_frames - 1)
        frame = cv2.addWeighted(img1, 1 - alpha, img2, alpha, 0)
        frames.append(Image.fromarray(frame))
    
    return frames

def generate_transition_frames(image1, image2, prompt, num_frames=16):
    """Generate transition frames using AI"""
    global pipe
    
    frames = []
    
    if pipe is None:
        print("⚠️ Using basic interpolation (models not loaded)")
        return interpolate_frames(image1, image2, num_frames)
    
    try:
        # Resize images to optimal size
        target_size = (512, 512)
        img1 = image1.resize(target_size)
        img2 = image2.resize(target_size)
        
        # Generate intermediate frames using the prompt
        for i in range(num_frames):
            alpha = i / (num_frames - 1)
            
            if i == 0:
                frames.append(img1)
            elif i == num_frames - 1:
                frames.append(img2)
            else:
                # Blend images for guidance
                blend_img = Image.blend(img1, img2, alpha)
                
                # Generate frame with prompt guidance
                modified_prompt = f"{prompt}, smooth transition, frame {i}/{num_frames}"
                
                with torch.no_grad():
                    generated = pipe(
                        modified_prompt,
                        image=blend_img,
                        num_inference_steps=20,
                        image_guidance_scale=1.5,
                        guidance_scale=7.5,
                    ).images[0]
                
                frames.append(generated)
                
            print(f"Generated frame {i+1}/{num_frames}")
    
    except Exception as e:
        print(f"⚠️ Error in AI generation: {e}")
        print("⚠️ Falling back to basic interpolation")
        return interpolate_frames(image1, image2, num_frames)
    
    return frames

def frames_to_video(frames, output_path, fps=8):
    """Convert frames to video file"""
    if not frames:
        raise ValueError("No frames to convert")
    
    # Get frame size
    frame = np.array(frames[0])
    height, width = frame.shape[:2]
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Write frames
    for frame in frames:
        frame_array = np.array(frame)
        frame_bgr = cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)
        out.write(frame_bgr)
    
    out.release()
    print(f"✅ Video saved to {output_path}")

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Generate video from two images and prompt"""
    try:
        # Get uploaded images
        if 'image1' not in request.files or 'image2' not in request.files:
            return jsonify({'error': 'Please upload both start and end images'}), 400
        
        image1_file = request.files['image1']
        image2_file = request.files['image2']
        prompt = request.form.get('prompt', 'smooth transition')
        num_frames = int(request.form.get('num_frames', 16))
        fps = int(request.form.get('fps', 8))
        
        # Load images
        image1 = Image.open(image1_file).convert('RGB')
        image2 = Image.open(image2_file).convert('RGB')
        
        print(f"🎬 Generating video: '{prompt}' ({num_frames} frames @ {fps} fps)")
        
        # Generate transition frames
        frames = generate_transition_frames(image1, image2, prompt, num_frames)
        
        # Create temporary video file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            video_path = tmp_file.name
        
        # Convert frames to video
        frames_to_video(frames, video_path, fps)
        
        # Read video and encode to base64
        with open(video_path, 'rb') as f:
            video_data = f.read()
            video_base64 = base64.b64encode(video_data).decode('utf-8')
        
        # Clean up
        os.remove(video_path)
        
        return jsonify({
            'success': True,
            'video': video_base64,
            'message': f'Generated {num_frames} frames successfully!'
        })
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'device': device,
        'model_loaded': pipe is not None
    })

if __name__ == '__main__':
    # Initialize models on startup
    initialize_models()
    
    # Run the app
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
