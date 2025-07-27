import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-approval',
  templateUrl: './approval.component.html'
})
export class ApprovalComponent {
  sbomId: number = 0;
  approved: boolean = false;
  notes: string = '';
  loading: boolean = false;
  
  
  approvals: any[] = [];


  constructor(private api: ApiService, private snackBar: MatSnackBar) {}
  

  ngOnInit() {
    this.fetchApprovals();
  }
  
  fetchApprovals() {
    this.api.getApprovals().subscribe({
      next: (data) => (this.approvals = data),
      error: () => this.snackBar.open('Failed to load approvals.', 'Close', { duration: 3000 })
    });
  }
  
  submit() {
    if (!this.sbomId) {
      this.snackBar.open('Please enter a valid SBOM ID.', 'Close', { duration: 3000 });
      return;
    }

    const payload = {
      sbom_id: this.sbomId,
      approved: this.approved,
      notes: this.notes
    };

    this.loading = true;

    this.api.submitApproval(payload).subscribe({
      next: () => {
        this.snackBar.open('Approval submitted!', 'Close', { duration: 3000 });
        this.resetForm();
      },
      error: () => {
        this.snackBar.open('Submission failed.', 'Close', { duration: 3000 });
        this.loading = false;
      }
    });
  }

  resetForm() {
    this.sbomId = 0;
    this.approved = false;
    this.notes = '';
    this.loading = false;
  }
}