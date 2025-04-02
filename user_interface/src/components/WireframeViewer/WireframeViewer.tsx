"use client";

import { Canvas, useLoader } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader";
import * as THREE from "three";
import { useMemo, useState } from "react";
import { Box, Typography, IconButton } from "@mui/material";
import GridOnIcon from "@mui/icons-material/GridOn";
import GridOffIcon from "@mui/icons-material/GridOff";

const labelColors: Record<number, string | null> = {
    0: "#ff0000",  1: "#ff7300", 2: "#ffbf00", 3: "#d4ff00", 4: "#66ff00",
    5: "#00ff33",  6: "#00ffbf", 7: "#00bfff", 8: "#0066ff", 9: "#0000ff",
    10: "#7300ff", 11: "#bf00ff", 12: "#ff00bf", 13: "#ff0066", 14: "#ff0033",
    15: "#800000", 16: "#804000", 17: "#808000", 18: "#408000", 19: "#008040",
    20: "#008080", 21: "#004080", 22: "#000080", 23: "#400080", 24: null
};

interface WireframeViewerProps {
    fileUrl: string;
    features: number[][];
    predictedLabels: number[];
}

export default function WireframeViewer({ fileUrl, features, predictedLabels }: WireframeViewerProps) {
    const [isWireframe, setIsWireframe] = useState(true);

    const toggleWireframe = () => {
        setIsWireframe((prev) => !prev);
    };

    return (
        <Box
            sx={{
                width: "40vw",
                minWidth: "300px",
                height: "40vw",
                maxHeight: "400px",
                borderRadius: 2,
                overflow: "hidden",
                bgcolor: "#787474",
                boxShadow: "3px 3px 10px rgba(0,0,0,0.2)",
                margin: "auto",
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
                    sx={{ position: "absolute", right: 8 }}
                >
                    {isWireframe ? <GridOffIcon /> : <GridOnIcon />}
                </IconButton>
            </Box>
            <Canvas
                camera={{ position: [50, 50, 50], fov: 45 }}
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
                <OrbitControls />
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
    // Immer `useMemo` aufrufen, auch wenn die Eingaben leer sind
    const vertices = useMemo(() => {
        if (!features.length || !predictedLabels.length) return [];
        return features
            .map((coord, index) => {
                if (predictedLabels[index] === 24) return null;
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
                    <sphereGeometry args={[0.5, 16, 16]} />
                    <meshStandardMaterial color={v!.color} />
                </mesh>
            ))}
        </>
    );
}

