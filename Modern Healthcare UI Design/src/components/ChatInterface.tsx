import { useState } from 'react';
import { Send, Mic, Paperclip } from 'lucide-react';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';

interface ChatInterfaceProps {
  onSendMessage: (message: string) => void;
  messages: Array<{ role: 'user' | 'assistant'; content: string }>;
}

export function ChatInterface({ onSendMessage }: ChatInterfaceProps) {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim()) {
      onSendMessage(input);
      setInput('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="bg-white border-t border-slate-200 px-8 py-6">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-end gap-3">
          <Button
            variant="outline"
            size="icon"
            className="h-12 w-12 rounded-xl border-slate-300 hover:bg-slate-100"
          >
            <Paperclip className="w-5 h-5 text-slate-600" />
          </Button>
          
          <div className="flex-1 relative">
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me about symptoms, appointments, or reminders..."
              className="min-h-[56px] max-h-32 resize-none rounded-xl border-slate-300 pr-12 py-4 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              rows={1}
            />
            <Button
              variant="ghost"
              size="icon"
              className="absolute right-2 bottom-2 h-8 w-8 rounded-lg hover:bg-slate-100"
            >
              <Mic className="w-4 h-4 text-slate-600" />
            </Button>
          </div>
          
          <Button
            onClick={handleSend}
            disabled={!input.trim()}
            className="h-12 px-6 rounded-xl bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 shadow-lg shadow-blue-500/30"
          >
            <Send className="w-5 h-5" />
          </Button>
        </div>
        
        <p className="text-xs text-slate-500 text-center mt-3">
          AI Assistant can make mistakes. Please verify important information.
        </p>
      </div>
    </div>
  );
}
