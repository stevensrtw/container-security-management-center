retryScan() {
  this.loading = true;
  this.api.retryScan(this.sbomId).subscribe({
    next: () => {
      this.snackBar.open('Scan retry queued.', 'Close', { duration: 3000 });
      this.loading = false;
    },
    error: err => {
      this.snackBar.open(err.error?.detail || 'Retry failed.', 'Close', { duration: 4000 });
      this.loading = false;
    }
  });
}