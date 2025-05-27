"use client";

import React, { useRef, useState } from "react";
import { Box } from "@mui/material";

const VideoPlayer = ({ src }: { src: string }) => {
    const videoRef = useRef<HTMLVideoElement>(null);
    const [isPlaying, setIsPlaying] = useState(false);

    const handleClick = () => {
        if (videoRef.current) {
            if (isPlaying) {
                videoRef.current.pause();
            } else {
                videoRef.current.play();
            }
            setIsPlaying(!isPlaying);
        }
    };

    return (
        <Box
            sx={{
                cursor: "pointer",
                width: "100%",
                borderRadius: "8px",
                overflow: "hidden",
                border: "2px solid #fff"
            }}
            onClick={handleClick}
        >
            <video
                ref={videoRef}
                src={src}
                style={{ width: "100%", height: "auto", display: "block" }}
                controls={false}
            />
        </Box>
    );
};

export default VideoPlayer;
