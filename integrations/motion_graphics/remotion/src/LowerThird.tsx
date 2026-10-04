import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export type LowerThirdProps = {
  name: string;
  subtitle: string;
  accent: string;
  text: string;
  fontFamily: string;
};

export const lowerThirdDefaults: LowerThirdProps = {
  name: "Character Name",
  subtitle: "Role or place",
  accent: "#E8B04B",
  text: "#F4F1EA",
  fontFamily: "Noto Sans, Noto Sans Devanagari, sans-serif",
};

// Rendered with a transparent background (ProRes 4444 / WebM VP9 alpha) and
// composited over the shot in the edit.
export const LowerThird: React.FC<LowerThirdProps> = (props) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const slide = interpolate(frame, [0, 10, durationInFrames - 10, durationInFrames], [-600, 0, 0, -600], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", padding: 96, fontFamily: props.fontFamily }}>
      <div style={{ transform: `translateX(${slide}px)`, borderLeft: `8px solid ${props.accent}`, paddingLeft: 24 }}>
        <div style={{ fontSize: 56, fontWeight: 700, color: props.text }}>{props.name}</div>
        <div style={{ fontSize: 32, color: props.accent }}>{props.subtitle}</div>
      </div>
    </AbsoluteFill>
  );
};
