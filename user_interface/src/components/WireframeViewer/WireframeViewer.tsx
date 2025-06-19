"use client";

import { Canvas, useLoader } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader";
import * as THREE from "three";
import { useMemo, useRef, useState, useEffect } from "react";
import { Box, Typography, IconButton } from "@mui/material";
import GridOnIcon from "@mui/icons-material/GridOn";
import GridOffIcon from "@mui/icons-material/GridOff";
import FullscreenIcon from "@mui/icons-material/Fullscreen";
import FullscreenExitIcon from "@mui/icons-material/FullscreenExit";

const labelColors: Record<number, string | null> = {
    0: "#e6194b", 1: "#3cb44b", 2: "#ffe119", 3: "#4363d8",
    4: "#000000", 5: "#f58231", 6: "#46f0f0", 7: "#f032e6", 8: "#000000"
};

interface WireframeViewerProps {
    fileUrl: string;
    features: number[][];
    predictedLabels: number[];
}

export default function WireframeViewer({ fileUrl, features, predictedLabels }: WireframeViewerProps) {
    const [isWireframe, setIsWireframe] = useState(false);
    const [isFullscreen, setIsFullscreen] = useState(false);
    const viewerRef = useRef<HTMLDivElement>(null);

    const toggleWireframe = () => setIsWireframe(prev => !prev);

    const toggleFullscreen = () => {
        if (!document.fullscreenElement && viewerRef.current) {
            viewerRef.current.requestFullscreen();
        } else if (document.fullscreenElement) {
            document.exitFullscreen();
        }
    };

    useEffect(() => {
        const handleChange = () => setIsFullscreen(!!document.fullscreenElement);
        document.addEventListener("fullscreenchange", handleChange);
        return () => document.removeEventListener("fullscreenchange", handleChange);
    }, []);

    return (
        <Box
            ref={viewerRef}
            sx={{
                width: isFullscreen ? "100vw" : "40vw",
                height: isFullscreen ? "100vh" : "40vw",
                maxHeight: isFullscreen ? "100vh" : "400px",
                position: "relative",
                borderRadius: 2,
                overflow: "hidden",
                bgcolor: "#787474",
                boxShadow: "3px 3px 10px rgba(0,0,0,0.2)",
                margin: "auto",
                transition: "all 0.3s ease"
            }}
        >
            <Box
                sx={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    padding: "8px 16px",
                    backgroundColor: "#787474",
                    position: "relative"
                }}
            >
                <Typography
                    align="center"
                    variant="h6"
                    sx={{ fontWeight: "bold", color: "white" }}
                >
                    Model Viewer
                </Typography>
                <IconButton
                    onClick={toggleWireframe}
                    color="primary"
                    size="small"
                    sx={{ position: "absolute", right: 48 }}
                >
                    {isWireframe ? <GridOffIcon /> : <GridOnIcon />}
                </IconButton>
                <IconButton
                    onClick={toggleFullscreen}
                    color="primary"
                    size="small"
                    sx={{ position: "absolute", right: 8 }}
                >
                    {isFullscreen ? <FullscreenExitIcon /> : <FullscreenIcon />}
                </IconButton>
            </Box>
            <Canvas
                camera={{ position: [8000, 5000, 1600], fov: 100, near: 1, far: 50000 }}
                shadows
                style={{ background: "whitesmoke", width: "100%", height: "90%" }}
            >
                <ambientLight intensity={1} color={"#ffffff"} />
                <spotLight position={[15, 30, 15]} intensity={1.0} color={"#ffffff"} angle={0.5} penumbra={0.5} />
                <directionalLight position={[-20, 20, 10]} intensity={0.7} color={"#f0f0f0"} />
                <pointLight position={[-15, -15, -15]} intensity={0.4} color={"#ff7820"} />
                <hemisphereLight groundColor={"#444444"} intensity={0.3} />

                {fileUrl && <WireframeSTLMesh fileUrl={fileUrl} isWireframe={isWireframe} />}
                {features && predictedLabels && (
                    <LabeledVertices features={features} predictedLabels={predictedLabels} />
                )}
                <OrbitControls target={[8000, 0, 1600]} />
            </Canvas>
        </Box>
    );
}

function WireframeSTLMesh({ fileUrl, isWireframe }: { fileUrl: string, isWireframe: boolean }) {
    const geometry = useLoader(STLLoader, fileUrl) as THREE.BufferGeometry;

    return (
        <mesh>
            <primitive object={geometry} attach="geometry" />
            <meshStandardMaterial
                color="#ff7820"
                wireframe={isWireframe}
                opacity={1}
                transparent={false}
                roughness={0.3}
                metalness={0.5}
            />
        </mesh>
    );
}

function LabeledVertices({ features, predictedLabels }: { features: number[][]; predictedLabels: number[] }) {
    const vertices = useMemo(() => {
        if (!features.length || !predictedLabels.length) return [];
        return features
            .map((coord, index) => {
                if (predictedLabels[index] === 8) return null;
                return {
                    position: new THREE.Vector3(coord[0], coord[1], coord[2]),
                    color: labelColors[predictedLabels[index] % 25] || "#ffffff"
                };
            })
            .filter(v => v !== null);
    }, [features, predictedLabels]);

    if (!vertices.length) return null;

    return (
        <>
            {vertices.map((v, i) => (
                <mesh key={i} position={[v!.position.x, v!.position.y, v!.position.z]}>
                    <sphereGeometry args={[100, 16, 16]} />
                    <meshStandardMaterial color={v!.color} />
                </mesh>
            ))}
        </>
    );
}
