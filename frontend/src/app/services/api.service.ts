import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private baseUrl = 'http://localhost:8000'; // your FastAPI backend
  private headers = new HttpHeaders({ 'Content-Type': 'application/json' });

  constructor(private http: HttpClient) {}

  uploadSBOM(sbom: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/sbom/upload`, sbom, { headers: this.headers });
  }

  listSBOMs(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/sbom/list`);
  }

  submitScan(scan: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/scan/submit`, scan, { headers: this.headers });
  }

  submitApproval(approval: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/approval/submit`, approval, { headers: this.headers });
  }

  pushToEmass(): Observable<any> {
    return this.http.post(`${this.baseUrl}/emass/push`, {}, { headers: this.headers });
  }
  
  getApprovals() {
  return this.http.get<any[]>('/api/approval/list'); // adjust endpoint if needed
  }
}