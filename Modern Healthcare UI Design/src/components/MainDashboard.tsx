import { Activity, Stethoscope, Calendar, Bell, Clock, Pill, AlertCircle } from 'lucide-react';
import { Badge } from './ui/badge';
import { Card } from './ui/card';
import { ScrollArea } from './ui/scroll-area';

interface MainDashboardProps {
  selectedPatient: string;
  isLocalMode: boolean;
  messages: Array<{ role: 'user' | 'assistant'; content: string }>;
}

export function MainDashboard({ selectedPatient, isLocalMode, messages }: MainDashboardProps) {
  const sampleQueries = [
    {
      category: 'Medical Triage',
      icon: Stethoscope,
      color: 'rose',
      queries: [
        'My child has fever and cough',
        'I have chest pain and difficulty breathing',
        'Minor cut, should I come in?'
      ]
    },
    {
      category: 'Appointments',
      icon: Calendar,
      color: 'blue',
      queries: [
        'Book appointment for next Tuesday',
        'Check availability for pediatrics',
        'Cancel my appointment'
      ]
    },
    {
      category: 'Information',
      icon: Bell,
      color: 'amber',
      queries: [
        'Show my upcoming appointments',
        'Set a medication reminder',
        'When is my next checkup?'
      ]
    }
  ];

  return (
    <div className="flex-1 overflow-hidden flex flex-col">
      {/* Header */}
      <div className="bg-white border-b border-slate-200 px-8 py-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-500 via-blue-600 to-purple-600 flex items-center justify-center shadow-lg">
              <Activity className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className="text-slate-900">Hospital AI Assistant</h1>
              <p className="text-sm text-slate-500">Intelligent Healthcare Support</p>
            </div>
          </div>
          <Badge variant="secondary" className="bg-blue-50 text-blue-700 border-blue-200">
            <Clock className="w-3 h-3 mr-1" />
            {new Date().toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })}
          </Badge>
        </div>
        
        <div className="flex items-center gap-3 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl border border-blue-100">
          <div className="w-8 h-8 rounded-lg bg-white flex items-center justify-center shadow-sm">
            <Activity className="w-4 h-4 text-blue-600" />
          </div>
          <div className="flex-1">
            <p className="text-sm text-slate-900">
              Current Patient: <span className="text-blue-600">{selectedPatient}</span>
            </p>
          </div>
          <Badge variant="outline" className={isLocalMode ? 'bg-green-50 text-green-700 border-green-300' : 'bg-slate-50 text-slate-700 border-slate-300'}>
            Mode: {isLocalMode ? 'Local Testing' : 'Production'}
          </Badge>
        </div>
      </div>

      {/* Main Content */}
      <ScrollArea className="flex-1">
        <div className="px-8 py-8">
          {messages.length === 0 ? (
            <div className="space-y-8">
              {/* Welcome Message */}
              <div className="text-center py-8">
                <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-blue-100 to-purple-100 mb-4">
                  <Activity className="w-10 h-10 text-blue-600" />
                </div>
                <h2 className="text-slate-900 mb-2">Welcome to Hospital AI Assistant</h2>
                <p className="text-slate-600 max-w-2xl mx-auto">
                  I'm here to help you with medical triage, appointment scheduling, medication reminders, and more. 
                  Try one of the sample queries below or ask me anything.
                </p>
              </div>

              {/* Sample Queries */}
              <div>
                <div className="flex items-center gap-2 mb-6">
                  <AlertCircle className="w-5 h-5 text-blue-600" />
                  <h3 className="text-slate-900">Try These Sample Queries</h3>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {sampleQueries.map((category) => {
                    const Icon = category.icon;
                    return (
                      <Card key={category.category} className="p-6 hover:shadow-lg transition-shadow border-slate-200">
                        <div className="flex items-center gap-3 mb-4">
                          <div className={`w-10 h-10 rounded-xl bg-gradient-to-br from-${category.color}-100 to-${category.color}-200 flex items-center justify-center`}>
                            <Icon className={`w-5 h-5 text-${category.color}-600`} />
                          </div>
                          <h4 className="text-slate-900">{category.category}</h4>
                        </div>
                        <ul className="space-y-3">
                          {category.queries.map((query, idx) => (
                            <li key={idx}>
                              <button className="w-full text-left p-3 rounded-lg bg-slate-50 hover:bg-slate-100 transition-colors text-sm text-slate-700 border border-slate-200 hover:border-slate-300">
                                "{query}"
                              </button>
                            </li>
                          ))}
                        </ul>
                      </Card>
                    );
                  })}
                </div>
              </div>

              {/* Quick Actions */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8">
                <Card className="p-6 bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-xl bg-white shadow-sm flex items-center justify-center">
                      <Pill className="w-6 h-6 text-blue-600" />
                    </div>
                    <div>
                      <h4 className="text-slate-900 mb-1">Medication Management</h4>
                      <p className="text-sm text-slate-600">Set reminders and track prescriptions</p>
                    </div>
                  </div>
                </Card>

                <Card className="p-6 bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-xl bg-white shadow-sm flex items-center justify-center">
                      <Calendar className="w-6 h-6 text-purple-600" />
                    </div>
                    <div>
                      <h4 className="text-slate-900 mb-1">Appointment Scheduling</h4>
                      <p className="text-sm text-slate-600">Book, reschedule, or cancel appointments</p>
                    </div>
                  </div>
                </Card>
              </div>
            </div>
          ) : (
            <div className="space-y-4 max-w-4xl mx-auto">
              {messages.map((message, idx) => (
                <div
                  key={idx}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[70%] p-4 rounded-2xl ${
                      message.role === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-white border border-slate-200 text-slate-900'
                    }`}
                  >
                    {message.content}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </ScrollArea>
    </div>
  );
}
