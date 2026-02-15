import os
import io
import base64
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image
import cv2
import tempfile
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

def apply_easing(t, easing_type='ease_in_out'):
    """Apply easing function for smoother transitions"""
    if easing_type == 'linear':
        return t
    elif easing_type == 'ease_in':
        return t * t
    elif easing_type == 'ease_out':
        return t * (2 - t)
    elif easing_type == 'ease_in_out':
        return t * t * (3 - 2 * t)  # Smooth hermite interpolation
    return t

def warp_flow(img, flow):
    """Warp image using optical flow"""
    h, w = flow.shape[:2]
    flow_map = np.copy(flow)
    flow_map[:, :, 0] += np.arange(w)
    flow_map[:, :, 1] += np.arange(h)[:, np.newaxis]
    
    warped = cv2.remap(img, flow_map, None, cv2.INTER_LINEAR)
    return warped

def interpolate_frames_smooth(image1, image2, num_frames=16):
    """Advanced frame interpolation with optical flow - Gemini Flow style"""
    frames = []
    
    # Convert PIL to numpy
    img1 = np.array(image1)
    img2 = np.array(image2)
    
    # Ensure same size (512x512 for consistency)
    target_size = (512, 512)
    img1 = cv2.resize(img1, target_size)
    img2 = cv2.resize(img2, target_size)
    
    # Convert to float for better processing
    img1_float = img1.astype(np.float32)
    img2_float = img2.astype(np.float32)
    
    # Convert to grayscale for optical flow
    gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    
    # Calculate bidirectional optical flow for better results
    flow_forward = cv2.calcOpticalFlowFarneback(
        gray1, gray2, None, 
        pyr_scale=0.5, levels=3, winsize=15, 
        iterations=3, poly_n=5, poly_sigma=1.2, flags=0
    )
    
    flow_backward = cv2.calcOpticalFlowFarneback(
        gray2, gray1, None,
        pyr_scale=0.5, levels=3, winsize=15,
        iterations=3, poly_n=5, poly_sigma=1.2, flags=0
    )
    
    # Generate interpolated frames with advanced blending
    for i in range(num_frames):
        # Use easing for smoother motion
        t = i / (num_frames - 1)
        alpha = apply_easing(t, 'ease_in_out')
        
        if i == 0:
            frames.append(Image.fromarray(img1))
        elif i == num_frames - 1:
            frames.append(Image.fromarray(img2))
        else:
            # Warp images based on flow
            flow_scaled_forward = flow_forward * alpha
            flow_scaled_backward = flow_backward * (1 - alpha)
            
            # Warp both images
            warped1 = warp_flow(img1_float, flow_scaled_forward)
            warped2 = warp_flow(img2_float, flow_scaled_backward)
            
            # Blend warped images
            blended = cv2.addWeighted(warped1, 1 - alpha, warped2, alpha, 0)
            
            # Add cross-fade for color consistency
            cross_fade = cv2.addWeighted(img1_float, 1 - alpha, img2_float, alpha, 0)
            
            # Combine warped and cross-faded for best results
            final = cv2.addWeighted(blended, 0.7, cross_fade, 0.3, 0)
            
            # Apply bilateral filter for smoothness while preserving edges
            final = cv2.bilateralFilter(final.astype(np.uint8), 5, 50, 50)
            
            # Enhance sharpness slightly
            kernel = np.array([[-0.5, -0.5, -0.5],
                             [-0.5,  5.0, -0.5],
                             [-0.5, -0.5, -0.5]])
            sharpened = cv2.filter2D(final, -1, kernel * 0.1)
            final = cv2.addWeighted(final, 0.85, sharpened, 0.15, 0)
            
            frames.append(Image.fromarray(final.astype(np.uint8)))
        
        print(f"Generated frame {i+1}/{num_frames}")
    
    return frames

def frames_to_video(frames, output_path, fps=8):
    """Convert frames to video file"""
    if not frames:
        raise ValueError("No frames to convert")
    
    # Get frame size
    frame = np.array(frames[0])
    height, width = frame.shape[:2]
    
    # Create video writer with better codec
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
    """Generate video from two images"""
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
        frames = interpolate_frames_smooth(image1, image2, num_frames)
        
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
        'mode': 'lightweight'
    })

if __name__ == '__main__':
    print("🚀 Starting AI Flow (Lightweight Mode)")
    print("⚡ Using CPU with optimized interpolation")
    
    # Run the app
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
