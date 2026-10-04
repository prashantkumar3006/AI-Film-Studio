import React from "react";
import { Composition } from "remotion";
import { TitleCard, titleCardDefaults } from "./TitleCard";
import { LowerThird, lowerThirdDefaults } from "./LowerThird";

// 24 fps to match the episode. Durations are defaults; the studio passes
// props (title, colours, durationInFrames) per episode via --props.
export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="TitleCard"
      component={TitleCard}
      durationInFrames={120}
      fps={24}
      width={1920}
      height={1080}
      defaultProps={titleCardDefaults}
    />
    <Composition
      id="LowerThird"
      component={LowerThird}
      durationInFrames={96}
      fps={24}
      width={1920}
      height={1080}
      defaultProps={lowerThirdDefaults}
    />
  </>
);
