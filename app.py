import os
import io
import base64
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image
import cv2
import tempfile
import gc

app = Flask(__name__)
CORS(app)

def apply_easing(t, easing_type='ease_in_out'):
    """Apply easing function"""
    if easing_type == 'ease_in_out':
        return t * t * (3 - 2 * t)
    return t

def interpolate_frames_smooth(image1, image2, num_frames=12):
    """Memory-optimized frame interpolation"""
    frames = []
    
    # Convert and resize to smaller size for memory efficiency
    img1 = np.array(image1.resize((384, 384)))
    img2 = np.array(image2.resize((384, 384)))
    
    img1_float = img1.astype(np.float32)
    img2_float = img2.astype(np.float32)
    
    # Calculate optical flow
    gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    
    flow = cv2.calcOpticalFlowFarneback(
        gray1, gray2, None,
        pyr_scale=0.5, levels=2, winsize=10,
        iterations=2, poly_n=5, poly_sigma=1.1, flags=0
    )
    
    # Generate frames
    for i in range(num_frames):
        t = i / (num_frames - 1)
        alpha = apply_easing(t)
        
        if i == 0:
            frames.append(Image.fromarray(img1))
        elif i == num_frames - 1:
            frames.append(Image.fromarray(img2))
        else:
            # Simple blend with flow guidance
            blended = cv2.addWeighted(img1_float, 1 - alpha, img2_float, alpha, 0)
            blended = blended.astype(np.uint8)
            frames.append(Image.fromarray(blended))
        
        # Force garbage collection
        if i % 4 == 0:
            gc.collect()
    
    return frames

def frames_to_video(frames, output_path, fps=8):
    """Convert frames to video"""
    if not frames:
        raise ValueError("No frames")
    
    frame = np.array(frames[0])
    height, width = frame.shape[:2]
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    for frame in frames:
        frame_array = np.array(frame)
        frame_bgr = cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)
        out.write(frame_bgr)
    
    out.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        if 'image1' not in request.files or 'image2' not in request.files:
            return jsonify({'error': 'Please upload both images'}), 400
        
        image1_file = request.files['image1']
        image2_file = request.files['image2']
        num_frames = min(int(request.form.get('num_frames', 12)), 16)  # Limit frames
        fps = int(request.form.get('fps', 8))
        
        # Load images
        image1 = Image.open(image1_file).convert('RGB')
        image2 = Image.open(image2_file).convert('RGB')
        
        print(f"🎬 Generating {num_frames} frames @ {fps} fps")
        
        # Generate frames
        frames = interpolate_frames_smooth(image1, image2, num_frames)
        
        # Create video
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            video_path = tmp_file.name
        
        frames_to_video(frames, video_path, fps)
        
        # Read and encode
        with open(video_path, 'rb') as f:
            video_data = f.read()
            video_base64 = base64.b64encode(video_data).decode('utf-8')
        
        # Cleanup
        os.remove(video_path)
        del frames
        gc.collect()
        
        return jsonify({
            'success': True,
            'video': video_base64,
            'message': f'Generated {num_frames} frames!'
        })
    
    except Exception as e:
        print(f"❌ Error: {e}")
        gc.collect()
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'mode': 'lightweight'})

if __name__ == '__main__':
    print("🚀 Starting AI Flow (Memory Optimized)")
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
