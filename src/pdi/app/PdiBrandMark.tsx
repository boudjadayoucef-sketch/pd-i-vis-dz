import React, { useState } from "react";

// PD&I — Logo officiel servi depuis /public.
const HORIZONTAL_LOGOS = [
  '/pdi-logo-horizontal.png',
  '/pdi-logo-horizontal.jpg',
  '/pdi-logo-horizental.jpeg',
  '/logo_pdi_horizontal.png',
  '/pdi_horizontal.png'
];
const SQUARE_LOGOS = [
  '/pdi-logo-square.png',
  '/pdi-logo-square.jpg',
  '/pdo-logo-square.jpeg',
  '/logo_pdi_square.png',
  '/pdi_square.png'
];

export type PdiBrandMarkProps = {
  variant?: "horizontal" | "compact";
  size?: "sm" | "md" | "lg";
  className?: string;
};

export default function PdiBrandMark({
  variant = "horizontal",
  size = "md",
  className = "",
}: PdiBrandMarkProps) {
  const compact = variant === "compact";
  const logos = compact ? SQUARE_LOGOS : HORIZONTAL_LOGOS;
  const [idx, setIdx] = useState(0);
  const height = size === "sm" ? 38 : size === "lg" ? 70 : 52;
  const src = logos[Math.min(idx, logos.length - 1)];

  return (
    <div className={`pdi-brand-mark ${className}`} aria-label="PD&I — Piping Design & Isometrics">
      <img
        src={src}
        alt="PD&I — Piping Design & Isometrics"
        onError={() => setIdx((value) => Math.min(value + 1, logos.length - 1))}
        style={{
          height,
          width: compact ? height : undefined,
          maxWidth: compact ? height : "min(330px, 34vw)",
          objectFit: "contain",
          display: "block",
        }}
        draggable={false}
      />
    </div>
  );
}
