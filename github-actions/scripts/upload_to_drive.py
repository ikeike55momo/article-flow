#!/usr/bin/env python3
"""Upload to Google Drive - Upload generated article and assets to Google Drive"""

import argparse
import sys
import os
import json
import mimetypes
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.logging_utils import setup_logging, log_phase_start, log_phase_end, log_error, log_metric
from utils.file_utils import read_json, write_json

# Google Drive imports
try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
except ImportError:
    print("Error: Google API client libraries not installed")
    print("Run: pip install google-api-python-client google-auth")
    sys.exit(1)


class GoogleDriveUploader:
    """Handle Google Drive uploads"""
    
    def __init__(self, credentials_json: str):
        """Initialize with service account credentials"""
        try:
            # Parse credentials from JSON string
            creds_data = json.loads(credentials_json)
            
            # Create credentials
            self.creds = Credentials.from_service_account_info(
                creds_data,
                scopes=['https://www.googleapis.com/auth/drive.file']
            )
            
            # Build service
            self.service = build('drive', 'v3', credentials=self.creds)
            
        except Exception as e:
            raise ValueError(f"Failed to initialize Google Drive service: {e}")
    
    def create_folder(
        self, 
        name: str, 
        parent_id: Optional[str] = None
    ) -> str:
        """Create a folder in Google Drive"""
        
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        if parent_id:
            file_metadata['parents'] = [parent_id]
        
        try:
            folder = self.service.files().create(
                body=file_metadata,
                fields='id',
                supportsAllDrives=True
            ).execute()
            
            return folder.get('id')
            
        except HttpError as e:
            raise Exception(f"Failed to create folder: {e}")
    
    def upload_file(
        self,
        file_path: Path,
        folder_id: str,
        file_name: Optional[str] = None,
        mime_type: Optional[str] = None
    ) -> Dict[str, str]:
        """Upload a file to Google Drive"""
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Determine file name and mime type
        if not file_name:
            file_name = file_path.name
        
        if not mime_type:
            mime_type, _ = mimetypes.guess_type(str(file_path))
            if not mime_type:
                mime_type = 'application/octet-stream'
        
        print(f"Uploading file '{file_name}' to folder ID: {folder_id}")
        
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        
        media = MediaFileUpload(
            str(file_path),
            mimetype=mime_type,
            resumable=True
        )
        
        try:
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink,webContentLink',
                supportsAllDrives=True
            ).execute()
            
            return {
                'id': file.get('id'),
                'name': file.get('name'),
                'webViewLink': file.get('webViewLink'),
                'webContentLink': file.get('webContentLink')
            }
            
        except HttpError as e:
            print(f"HttpError details: {e}")
            print(f"File: {file_name}")
            print(f"Folder ID: {folder_id}")
            print(f"File metadata: {file_metadata}")
            if hasattr(e, 'resp'):
                print(f"Response status: {e.resp.status}")
                print(f"Response reason: {e.resp.reason}")
            raise Exception(f"Failed to upload file {file_name} to folder {folder_id}: {e}")
    
    def set_permissions(
        self,
        file_id: str,
        permission_type: str = 'anyone',
        role: str = 'reader'
    ):
        """Set permissions on a file or folder"""
        
        permission = {
            'type': permission_type,
            'role': role
        }
        
        try:
            self.service.permissions().create(
                fileId=file_id,
                body=permission
            ).execute()
        except HttpError as e:
            # Log but don't fail if permission setting fails
            print(f"Warning: Failed to set permissions: {e}")


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Upload to Google Drive")
    parser.add_argument("--article-dir", required=True, help="Article output directory")
    parser.add_argument("--drive-folder-id", required=True, help="Google Drive folder ID")
    parser.add_argument("--public", action="store_true", help="Make files publicly accessible")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    return parser.parse_args()


def collect_files_to_upload(article_dir: Path) -> Dict[str, List[Path]]:
    """Collect all files to upload from article directory"""
    
    files = {
        "documents": [],
        "images": [],
        "reports": [],
        "metadata": []
    }
    
    # Document files
    for pattern in ["*.html", "*.md"]:
        files["documents"].extend(article_dir.glob(pattern))
    
    # Image files
    images_dir = article_dir / "images"
    if images_dir.exists():
        for pattern in ["*.png", "*.jpg", "*.jpeg", "*.webp"]:
            files["images"].extend(images_dir.glob(pattern))
    
    # Report files
    for pattern in ["*report*.json", "*metadata*.json"]:
        files["reports"].extend(article_dir.glob(pattern))
    
    # Other metadata
    for pattern in ["*.json"]:
        json_files = article_dir.glob(pattern)
        for f in json_files:
            if f not in files["reports"]:
                files["metadata"].append(f)
    
    return files


def create_folder_structure(
    uploader: GoogleDriveUploader,
    parent_folder_id: str,
    article_id: str
) -> Dict[str, str]:
    """Create folder structure in Google Drive"""
    
    import time
    
    # Create main article folder
    folder_name = f"{datetime.now().strftime('%Y-%m-%d')}_{article_id}"
    print(f"Creating main folder '{folder_name}' in parent folder ID: {parent_folder_id}")
    main_folder_id = uploader.create_folder(folder_name, parent_folder_id)
    print(f"Created main folder with ID: {main_folder_id}")
    
    # Wait a bit for folder creation to propagate
    time.sleep(2)
    
    # Create subfolders
    print(f"Creating subfolders in main folder ID: {main_folder_id}")
    folders = {
        "main": main_folder_id,
        "images": uploader.create_folder("images", main_folder_id),
        "reports": uploader.create_folder("reports", main_folder_id)
    }
    print(f"Created folder structure: {folders}")
    
    return folders


def upload_article_files(
    uploader: GoogleDriveUploader,
    files: Dict[str, List[Path]],
    folders: Dict[str, str],
    set_public: bool = False
) -> Dict[str, Any]:
    """Upload all article files to appropriate folders"""
    
    uploaded_files = {
        "documents": [],
        "images": [],
        "reports": [],
        "metadata": []
    }
    
    # Upload documents to main folder
    for doc_file in files["documents"]:
        result = uploader.upload_file(doc_file, folders["main"])
        uploaded_files["documents"].append(result)
        
        if set_public:
            uploader.set_permissions(result["id"])
    
    # Upload images
    for img_file in files["images"]:
        result = uploader.upload_file(img_file, folders["images"])
        uploaded_files["images"].append(result)
        
        if set_public:
            uploader.set_permissions(result["id"])
    
    # Upload reports
    for report_file in files["reports"]:
        result = uploader.upload_file(report_file, folders["reports"])
        uploaded_files["reports"].append(result)
    
    # Upload metadata
    for meta_file in files["metadata"]:
        result = uploader.upload_file(meta_file, folders["main"])
        uploaded_files["metadata"].append(result)
    
    return uploaded_files


def create_upload_summary(
    folders: Dict[str, str],
    uploaded_files: Dict[str, Any],
    article_metadata: Dict[str, Any]
) -> Dict[str, Any]:
    """Create a summary of the upload"""
    
    # Find main article file
    html_files = [f for f in uploaded_files["documents"] if f["name"].endswith(".html")]
    main_article_url = html_files[0]["webViewLink"] if html_files else None
    
    summary = {
        "upload_timestamp": datetime.utcnow().isoformat(),
        "folder_structure": folders,
        "main_article_url": main_article_url,
        "statistics": {
            "documents": len(uploaded_files["documents"]),
            "images": len(uploaded_files["images"]),
            "reports": len(uploaded_files["reports"]),
            "total_files": sum(len(files) for files in uploaded_files.values())
        },
        "article_info": {
            "title": article_metadata.get("title", ""),
            "topic": article_metadata.get("topic", ""),
            "word_count": article_metadata.get("total_word_count", 0),
            "quality_score": article_metadata.get("quality_score", 0),
            "factcheck_score": article_metadata.get("factcheck_score", 0)
        },
        "files": uploaded_files
    }
    
    return summary


def main():
    """Main execution function"""
    args = parse_arguments()
    
    # Setup logging
    logger = setup_logging("google_drive_upload", args.log_level)
    log_phase_start(logger, "Google Drive Upload")
    
    try:
        # Get credentials from environment
        creds_json = os.environ.get("GOOGLE_DRIVE_CREDENTIALS")
        if not creds_json:
            raise ValueError("GOOGLE_DRIVE_CREDENTIALS not found in environment")
        
        # Initialize uploader
        logger.info("Initializing Google Drive connection...")
        uploader = GoogleDriveUploader(creds_json)
        
        # Collect files
        article_dir = Path(args.article_dir)
        if not article_dir.exists():
            raise FileNotFoundError(f"Article directory not found: {article_dir}")
        
        files = collect_files_to_upload(article_dir)
        total_files = sum(len(file_list) for file_list in files.values())
        logger.info(f"Found {total_files} files to upload")
        
        # Read article metadata
        metadata_files = list(article_dir.glob("*metadata*.json"))
        article_metadata = {}
        if metadata_files:
            article_metadata = read_json(metadata_files[0])
        
        # Extract article ID
        article_id = article_dir.name
        
        # Create folder structure
        logger.info("Creating folder structure in Google Drive...")
        folders = create_folder_structure(
            uploader,
            args.drive_folder_id,
            article_id
        )
        
        # Upload files
        logger.info("Uploading files...")
        uploaded_files = upload_article_files(
            uploader,
            files,
            folders,
            args.public
        )
        
        # Set folder permissions if public
        if args.public:
            logger.info("Setting public permissions on main folder...")
            uploader.set_permissions(folders["main"])
        
        # Create upload summary
        summary = create_upload_summary(
            folders,
            uploaded_files,
            article_metadata
        )
        
        # Save summary locally
        summary_file = article_dir / "upload_summary.json"
        write_json(summary, summary_file)
        
        # Log metrics
        log_metric(logger, "files_uploaded", summary["statistics"]["total_files"])
        log_metric(logger, "images_uploaded", summary["statistics"]["images"])
        
        # Print summary
        logger.info(f"Upload completed successfully!")
        logger.info(f"Main article URL: {summary['main_article_url']}")
        logger.info(f"Total files uploaded: {summary['statistics']['total_files']}")
        
        log_phase_end(logger, "Google Drive Upload", success=True)
        
    except Exception as e:
        log_error(logger, e, "Google Drive Upload")
        log_phase_end(logger, "Google Drive Upload", success=False)
        sys.exit(1)


if __name__ == "__main__":
    main()