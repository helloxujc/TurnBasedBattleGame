import { useState, useEffect, useCallback, useRef } from 'react';
import { GameMessage, GameSession } from '../types/game';

interface UseWebSocketReturn {
  socket: WebSocket | null;
  connected: boolean;
  session: GameSession | null;
  sessionId: string | null;
  messages: GameMessage[];
  sendMessage: (message: any) => void;
  connect: () => void;
  disconnect: () => void;
  clearMessages: () => void;
}

export const useWebSocket = (url: string): UseWebSocketReturn => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [connected, setConnected] = useState(false);
  const [session, setSession] = useState<GameSession | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<GameMessage[]>([]);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const connect = useCallback(() => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      return;
    }

    const ws = new WebSocket(url);

    ws.onopen = () => {
      console.log('WebSocket connected');
      setConnected(true);
      setSocket(ws);
    };

    ws.onmessage = (event) => {
      try {
        const message: GameMessage = JSON.parse(event.data);
        console.log('Received message:', message);

        setMessages(prev => [...prev, message]);

        // Handle specific message types
        switch (message.type) {
          case 'game_started':
          case 'battle_started':
          case 'turn_result':
            if (message.session) {
              setSession(message.session);
            }
            break;
          case 'game_over':
            if (message.session) {
              setSession(message.session);
            }
            break;
        }
      } catch (error) {
        console.error('Error parsing message:', error);
      }
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setConnected(false);
      setSocket(null);

      // Auto-reconnect after 3 seconds
      reconnectTimeoutRef.current = setTimeout(() => {
        console.log('Attempting to reconnect...');
        connect();
      }, 3000) as NodeJS.Timeout;
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

  }, [url, socket]);

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }

    if (socket) {
      socket.close();
      setSocket(null);
    }

    setConnected(false);
    setSession(null);
    setSessionId(null);
  }, [socket]);

  const sendMessage = useCallback((message: any) => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify(message));
      console.log('Sent message:', message);
    } else {
      console.warn('WebSocket not connected, cannot send message');
    }
  }, [socket]);

  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  useEffect(() => {
    connect();

    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  return {
    socket,
    connected,
    session,
    sessionId,
    messages,
    sendMessage,
    connect,
    disconnect,
    clearMessages
  };
};