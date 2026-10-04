import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export type TitleCardProps = {
  series: string;
  episode: string;
  title: string;
  background: string;
  accent: string;
  text: string;
  fontFamily: string;
};

export const titleCardDefaults: TitleCardProps = {
  series: "SERIES TITLE",
  episode: "EPISODE 01",
  title: "Episode Title",
  background: "#0B0F1A",
  accent: "#E8B04B",
  text: "#F4F1EA",
  // Use only fonts you are licensed to use (e.g. OFL Google Fonts). Record them in legal/.
  fontFamily: "Noto Sans, Noto Sans Devanagari, sans-serif",
};

export const TitleCard: React.FC<TitleCardProps> = (props) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const enter = spring({ frame, fps, config: { damping: 200 } });
  const exit = interpolate(frame, [durationInFrames - 12, durationInFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const lineWidth = interpolate(frame, [6, 30], [0, 640], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: props.background,
        justifyContent: "center",
        alignItems: "center",
        fontFamily: props.fontFamily,
        color: props.text,
        opacity: exit,
      }}
    >
      <div style={{ fontSize: 36, letterSpacing: 12, opacity: enter, color: props.accent }}>{props.series}</div>
      <div style={{ width: lineWidth, height: 3, background: props.accent, margin: "28px 0" }} />
      <div style={{ fontSize: 30, letterSpacing: 8, opacity: enter }}>{props.episode}</div>
      <div
        style={{
          fontSize: 96,
          fontWeight: 700,
          marginTop: 18,
          transform: `translateY(${(1 - enter) * 40}px)`,
          opacity: enter,
        }}
      >
        {props.title}
      </div>
    </AbsoluteFill>
  );
};
