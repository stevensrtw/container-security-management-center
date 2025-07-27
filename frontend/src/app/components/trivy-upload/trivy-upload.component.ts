import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { LoginComponent } from './components/login/login.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { SBOMUploadComponent } from './components/sbom-upload/sbom-upload.component';
import { ScanResultsComponent } from './components/scan-results/scan-results.component';
import { CompareComponent } from './components/compare/compare.component';
import { ApprovalComponent } from './components/approval/approval.component';
import { FormsModule } from '@angular/forms';
import { MaterialModule } from './material.module';

@NgModule(import { Component, ElementRef, ViewChild } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-trivy-upload',
  templateUrl: './trivy-upload.component.html'
})
export class TrivyUploadComponent {
  imageName: string = '';
  loading = false;
  submitted = false;
  formInvalid = false;

  constructor(private api: ApiService, private snackBar: MatSnackBar) {}

  submit(container: ElementRef) {
    this.submitted = true;

    if (!this.imageName.trim()) {
      this.formInvalid = true;
      setTimeout(() => {
        const firstError = container.nativeElement.querySelector('.invalid');
        firstError?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 0);
      return;
    }

    this.loading = true;
    this.formInvalid = false;

    this.api.triggerTrivyScan({ image: this.imageName }).subscribe({
      next: () => {
        this.snackBar.open('Scan triggered successfully!', 'Close', { duration: 3000 });
        this.imageName = '';
        this.loading = false;
        this.submitted = false;
      },
      error: () => {
        this.snackBar.open('Failed to trigger scan.', 'Close', { duration: 3000 });
        this.loading = false;
      }
    });
  }
}
  declarations: [
    AppComponent,
    LoginComponent,
    DashboardComponent,
    SBOMUploadComponent,
    ScanResultsComponent,
    CompareComponent,
    ApprovalComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    MaterialModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }