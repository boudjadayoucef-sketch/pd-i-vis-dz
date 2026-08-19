import React from 'react';

interface NetworkAnimationProps {
  className?: string;
  onEnterApp?: () => void;
}

export const NetworkAnimation: React.FC<NetworkAnimationProps> = ({ className }) => {
  return (
    <div className={`relative w-full h-[520px] sm:h-[600px] lg:h-[650px] rounded-3xl overflow-hidden shadow-2xl border border-blue-500/20 bg-[#05060b] group ${className || ''}`}>
      <iframe
        src="/rtg-animation.html"
        title="Animation Réseau Gaz Algérie"
        className="w-full h-full border-0 overflow-hidden select-none"
        style={{ width: '100%', height: '100%', border: 'none', overflow: 'hidden' }}
        scrolling="no"
      />
    </div>
  );
};

