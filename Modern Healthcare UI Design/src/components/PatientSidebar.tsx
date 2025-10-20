import { User, Activity, Calendar, FileText } from 'lucide-react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Switch } from './ui/switch';
import { Label } from './ui/label';
import { Card } from './ui/card';
import { Separator } from './ui/separator';

interface PatientSidebarProps {
  selectedPatient: string;
  onPatientChange: (patient: string) => void;
  isLocalMode: boolean;
  onModeChange: (mode: boolean) => void;
  agentStats: {
    totalQueries: number;
    triageRequests: number;
    bookings: number;
  };
}

export function PatientSidebar({
  selectedPatient,
  onPatientChange,
  isLocalMode,
  onModeChange,
  agentStats
}: PatientSidebarProps) {
  const patients = [
    'Emma Johnson (Pediatric)',
    'Michael Smith (Cardiology)',
    'Sarah Williams (Orthopedic)',
    'James Brown (General)'
  ];

  return (
    <div className="w-80 bg-white border-r border-slate-200 flex flex-col shadow-sm">
      {/* Header */}
      <div className="p-6 border-b border-slate-200">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center shadow-lg">
            <Activity className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-slate-900">Health AI</h1>
            <p className="text-xs text-slate-500">Multi-Agent System</p>
          </div>
        </div>
      </div>

      {/* Patient Selection */}
      <div className="p-6 space-y-4">
        <div>
          <Label className="text-xs text-slate-600 mb-2 block">Patient Information</Label>
          <Select value={selectedPatient} onValueChange={onPatientChange}>
            <SelectTrigger className="w-full bg-slate-50 border-slate-200">
              <div className="flex items-center gap-2">
                <User className="w-4 h-4 text-blue-600" />
                <SelectValue />
              </div>
            </SelectTrigger>
            <SelectContent>
              {patients.map((patient) => (
                <SelectItem key={patient} value={patient}>
                  {patient}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <Separator />

        {/* Connection Mode */}
        <div>
          <Label className="text-xs text-slate-600 mb-3 block">Connection Mode</Label>
          <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-200">
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${isLocalMode ? 'bg-green-500' : 'bg-slate-400'} animate-pulse`} />
              <span className="text-sm text-slate-700">
                {isLocalMode ? 'Local Testing' : 'Production'}
              </span>
            </div>
            <Switch
              checked={isLocalMode}
              onCheckedChange={onModeChange}
            />
          </div>
        </div>

        <Separator />

        {/* Agent Statistics */}
        <div>
          <Label className="text-xs text-slate-600 mb-3 block">Agent Statistics</Label>
          <div className="space-y-2">
            <Card className="p-3 bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <FileText className="w-4 h-4 text-blue-600" />
                  <span className="text-sm text-slate-700">Total Queries</span>
                </div>
                <span className="text-blue-600">{agentStats.totalQueries}</span>
              </div>
            </Card>

            <Card className="p-3 bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Activity className="w-4 h-4 text-purple-600" />
                  <span className="text-sm text-slate-700">Triage Requests</span>
                </div>
                <span className="text-purple-600">{agentStats.triageRequests}</span>
              </div>
            </Card>

            <Card className="p-3 bg-gradient-to-br from-green-50 to-green-100 border-green-200">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Calendar className="w-4 h-4 text-green-600" />
                  <span className="text-sm text-slate-700">Bookings</span>
                </div>
                <span className="text-green-600">{agentStats.bookings}</span>
              </div>
            </Card>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="mt-auto p-6 border-t border-slate-200">
        <div className="text-xs text-slate-500 text-center">
          Powered by Multi-Agent AI
        </div>
      </div>
    </div>
  );
}
