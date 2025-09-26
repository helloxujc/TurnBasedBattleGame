import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders game title', () => {
  render(<App />);
  const titleElement = screen.getByText(/Turn-Based Battle Game/i);
  expect(titleElement).toBeInTheDocument();
});

test('shows connecting message', () => {
  render(<App />);
  const connectingElement = screen.getByText(/Connecting to server/i);
  expect(connectingElement).toBeInTheDocument();
});

test('renders main game container', () => {
  render(<App />);
  const gameContainer = document.querySelector('.game-container');
  expect(gameContainer).toBeInTheDocument();
});
