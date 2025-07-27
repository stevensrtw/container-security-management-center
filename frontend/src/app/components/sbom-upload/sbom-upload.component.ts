import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-sbom-upload',
  templateUrl: './sbom-upload.component.html'
})
export class SBOMUploadComponent {
  selectedFile: File | null = null;
  loading = false;

  constructor(private api: ApiService, private snackBar: MatSnackBar) {}

  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0];
  }

  upload(): void {
    if (!this.selectedFile) return;
    this.loading = true;

    const reader = new FileReader();
    reader.onload = () => {
      const content = reader.result as string;
      this.api.uploadSBOM({ name: this.selectedFile!.name, content }).subscribe({
        next: () => {
          this.snackBar.open('SBOM uploaded successfully!', 'Close', { duration: 3000 });
          this.selectedFile = null;
          this.loading = false;
        },
        error: () => {
          this.snackBar.open('Upload failed. Please try again.', 'Close', { duration: 3000 });
          this.loading = false;
        }
      });
    };
    reader.readAsText(this.selectedFile);
  }
}
