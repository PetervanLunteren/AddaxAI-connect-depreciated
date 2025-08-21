# EcoAssist-connect Project Documentation

## Project Overview
Real-time wildlife detection and notification system for camera trap images. Monitors image sources, runs AI inference, and sends alerts when animals are detected.

## Architecture

### Core Components
- **main.py**: Primary script with all detection and notification logic
- **run.py**: Wrapper that restarts main.py on errors
- **config.json**: Credentials and environment-specific settings

### Key Directories
- `/models/`: AI models (MegaDetector, DeepFaune, Namibian Desert)
- `/EcoAssist-connect-app/`: Additional app components
- `/mnt/volume_ams3_01/output/`: Project data and outputs
- `/var/ftps/camera/uploads/`: FTPS image upload directory

## Image Processing Pipeline

### Input Sources
1. **Gmail**: Monitors specific labels via IMAP
2. **FTPS**: Watches `/var/ftps/camera/uploads/`

### Detection Models
- **MegaDetector** (`md_v5a.0.0.pt`): General wildlife detection
- **DeepFaune** (`deepfaune-vit_large_patch14_dinov2.lvd142m.pt`): Species classification
- **Namibian Desert** (`namib_desert_v1.pt`): Desert-specific species

### Output Channels
- **WhatsApp**: Via Twilio API
- **Email**: Via Mailgun API  
- **EarthRanger**: Conservation management platform
- **Image Hosting**: ImgBB (Windows/Mac) or local nginx (Linux)

## Project Configuration

Each project has an Excel settings file at:
`/mnt/volume_ams3_01/output/{project_name}/data/settings.xlsx`

Contains:
- General settings and thresholds
- Species presence/absence lists with aliases
- Camera IMEI assignments
- Notification recipient preferences

## Key Functions

### Core Workflow
- `import_project_settings()`: Load all project configurations
- `predict_single_image()`: Run AI inference on image
- `postprocess()`: Generate visualizations and organize outputs
- `send_whatsapp()`, `send_email_plain()`: Send notifications
- `retrieve_project_name_from_imei()`: Map camera to project

### Utilities
- `fetch_img_exif()`: Extract metadata
- `fetch_lat_lon()`: Get GPS coordinates
- `read_gps_text_from_image()`: OCR for GPS text overlay
- `check_qr_code_contains_cv2()`: QR code validation
- `move_to_invalid_files_folder()`: Error handling

## File Management
- **admin_files.csv**: Tracks all processed images
- **log.txt**: Runtime logs in output directory
- Image files moved to project folders after processing
- Invalid files quarantined in `/invalid_files/`

## Dependencies
- PyTorch for model inference
- OpenCV for image processing
- Pillow for image manipulation
- Twilio SDK for WhatsApp
- Various utilities: pytesseract (OCR), piexif (EXIF), gpsphoto (GPS)

## Environment Variables
Platform-specific paths configured in config.json:
- `conda_dir_{platform}`: Conda installation
- `EcoAssist_files_{platform}`: Support files
- `file_storage_dir_linux`: Image storage (Linux only)
- `url_prefix_{platform}`: Image URL generation

## Error Handling
- Automatic retry with exponential backoff for network operations
- Script restart via run.py wrapper on crashes
- Invalid file quarantine system
- Comprehensive logging at each step

## Testing Commands
Check for existing test/lint commands in:
- package.json (if exists)
- Project documentation
- Shell scripts: `run_*.bat`, `run_*.command`

## Common Tasks
- Add new project: Create Excel file in output directory
- Update species list: Edit project's settings.xlsx
- Change notification recipients: Update WhatsApp/email sheets
- Debug issues: Check log.txt and set debug_mode in config.json
- Process backlog: Place images in FTPS folder or forward to Gmail

## Security Notes
- Credentials stored in config.json (gitignored)
- Images temporarily stored on public servers for sharing
- FTPS and Gmail credentials have app-specific passwords
- Twilio/Mailgun API keys should be kept secure