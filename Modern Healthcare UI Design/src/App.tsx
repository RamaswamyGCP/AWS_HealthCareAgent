import { useState } from 'react';
import { PatientSidebar } from './components/PatientSidebar';
import { MainDashboard } from './components/MainDashboard';
import { ChatInterface } from './components/ChatInterface';

export default function App() {
  const [selectedPatient, setSelectedPatient] = useState('Emma Johnson (Pediatric)');
  const [isLocalMode, setIsLocalMode] = useState(true);
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant'; content: string }>>([]);

  const agentStats = {
    totalQueries: 0,
    triageRequests: 0,
    bookings: 0
  };

  const handleSendMessage = (message: string) => {
    setMessages([...messages, { role: 'user', content: message }]);
    // Simulate AI response
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'I\'m your Hospital AI Assistant. How can I help you today?' 
      }]);
    }, 1000);
  };

  return (
    <div className="flex h-screen bg-slate-50">
      <PatientSidebar
        selectedPatient={selectedPatient}
        onPatientChange={setSelectedPatient}
        isLocalMode={isLocalMode}
        onModeChange={setIsLocalMode}
        agentStats={agentStats}
      />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <MainDashboard
          selectedPatient={selectedPatient}
          isLocalMode={isLocalMode}
          messages={messages}
        />
        
        <ChatInterface
          onSendMessage={handleSendMessage}
          messages={messages}
        />
      </div>
    </div>
  );
}
