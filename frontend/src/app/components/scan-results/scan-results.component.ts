import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-scan-results',
  templateUrl: './scan-results.component.html'
})
export class ScanResultsComponent implements OnInit {
  scanResults: any[] = [];

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.api.listSBOMs().subscribe(sboms => {
      this.scanResults = sboms.map(sbom => ({
        id: sbom.id,
        name: sbom.name,
        content: sbom.content
      }));
    });
  }
}
