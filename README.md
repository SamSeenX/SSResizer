# 🖼️ Image Resizer Pro

A professional, modern desktop application for batch image resizing with an intuitive dark-themed UI. Built with Python and Tkinter, Image Resizer Pro makes it easy to resize, crop, and convert images to standard resolutions.

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Features

### 🎯 Core Functionality
- **Batch Processing**: Process multiple images at once or one at a time
- **Smart Cropping**: Intelligent aspect ratio cropping with adjustable positioning
- **Multiple Resolutions**: Support for 480P, 720P, 1080P, 2K, and 4K
- **Dual Orientation**: Landscape and portrait mode support
- **Format Conversion**: Export to JPEG, PNG, or WEBP formats
- **Live Preview**: Real-time preview of cropped and resized images
- **Quality Control**: Adjustable JPEG quality settings (1-100)

### 🎨 User Interface
- **Modern Dark Theme**: Professional, eye-friendly interface
- **Intuitive Controls**: Easy-to-use sidebar with all settings
- **Visual Feedback**: Live preview with crop area visualization
- **Progress Tracking**: See which image you're on and how many remain
- **File Size Estimation**: Real-time output file size preview

### 🔧 Advanced Features
- **Precision Cropping**: Fine-tune horizontal and vertical crop positions
- **Uncropped Preview**: Small overlay showing the original image with crop area
- **Navigation Controls**: Previous, Skip, and Process & Next buttons
- **Batch Mode**: Process all remaining images with one click
- **Smart Defaults**: Sensible default settings for quick workflows

## 📸 Screenshots

### Main Interface
The application features a clean, modern interface with:
- Left sidebar for all settings and controls
- Large central preview area
- Top information bar showing file details
- Bottom action buttons for navigation and processing

### Supported Resolutions
| Resolution | Landscape | Portrait |
|------------|-----------|----------|
| 480P | 854 × 480 | 480 × 854 |
| 720P | 1280 × 720 | 720 × 1280 |
| 1080P | 1920 × 1080 | 1080 × 1920 |
| 2K | 2560 × 1440 | 1440 × 2560 |
| 4K | 3840 × 2160 | 2160 × 3840 |

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/image-resizer-pro.git
   cd image-resizer-pro
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python SSResizer.py
   ```

### Dependencies
- **Pillow (PIL)**: Image processing library
- **tkinter**: GUI framework (usually included with Python)

Create a `requirements.txt` file with:
```
Pillow>=9.0.0
```

## 📖 How to Use

### Basic Workflow

1. **Select a Folder**
   - Click "Select Folder" on the welcome screen
   - Choose a folder containing your images
   - Supported formats: PNG, JPG, JPEG, BMP, GIF, TIFF, WEBP

2. **Configure Settings**
   - **Resolution**: Choose from 480P to 4K
   - **Orientation**: Select Landscape or Portrait
   - **Output Format**: Pick JPEG, PNG, or WEBP
   - **JPEG Quality**: Adjust quality slider (JPEG only)

3. **Adjust Cropping** (Optional)
   - Use the crop sliders to fine-tune positioning
   - Landscape mode: Adjust vertical position (top/bottom)
   - Portrait mode: Adjust horizontal position (left/right)
   - Click "Reset to Center" to return to default

4. **Process Images**
   - **Process & Next**: Process current image and move to next
   - **Skip**: Skip current image without processing
   - **Previous**: Go back to previous image
   - **Process All**: Batch process all remaining images

5. **Find Your Images**
   - Processed images are saved in `SSResized` folder
   - Located inside your original image folder
   - Original images remain untouched

### Tips & Tricks

- **Preview Window**: The small overlay in the top-right shows the original image with the crop area highlighted
- **File Size Estimation**: Check the estimated output size in the info bar before processing
- **Batch Processing**: Use "Process All" for consistent settings across multiple images
- **Navigation**: Use Previous/Skip to review images before processing

## 🎨 Customization

### Color Scheme
The application uses a modern dark theme with customizable colors defined in the `colors` dictionary:
- Background: `#1a1a1a`
- Sidebar: `#252525`
- Primary: `#6366f1` (Indigo)
- Success: `#10b981` (Green)
- Accent: `#8b5cf6` (Purple)

### Adding Custom Resolutions
Edit the `resolutions` dictionary in `SSResizer.py`:
```python
self.resolutions = {
    "Custom": {"landscape": (1600, 900), "portrait": (900, 1600)},
    # Add more resolutions here
}
```

## 🛠️ Technical Details

### Architecture
- **Language**: Python 3.7+
- **GUI Framework**: Tkinter with custom Canvas-based widgets
- **Image Processing**: Pillow (PIL Fork)
- **Resampling**: Lanczos algorithm for high-quality resizing

### Key Components
- **ModernButton**: Custom Canvas-based button widget with hover effects
- **ImageResizerApp**: Main application class handling all functionality
- **Smart Cropping**: Automatic aspect ratio calculation and cropping
- **Live Preview**: Real-time image processing and display

### Performance
- Efficient memory usage with image streaming
- Optimized preview generation
- Fast batch processing
- Real-time file size calculation

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**SamSeen**

- GitHub: [@yourusername](https://github.com/yourusername)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Known Issues

- None currently reported

## 🔮 Future Enhancements

- [ ] Drag and drop support
- [ ] Custom resolution input
- [ ] Watermark support
- [ ] Image filters and effects
- [ ] Undo/Redo functionality
- [ ] Multi-language support
- [ ] Preset saving and loading
- [ ] Command-line interface
- [ ] Progress bar for batch processing
- [ ] Image metadata preservation

## 💡 Acknowledgments

- Built with [Pillow](https://python-pillow.org/) - The friendly PIL fork
- UI inspired by modern design principles
- Icons: Unicode emoji characters

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the documentation

---

<div align="center">
Made with ❤️ by SamSeen

⭐ Star this repo if you find it helpful!
</div>

