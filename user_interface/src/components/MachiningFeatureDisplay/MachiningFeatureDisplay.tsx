"use client";

import { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";

const labelColors: Record<number, string | null> = {
    0: "#e6194b", 1: "#3cb44b", 2: "#ffe119", 3: "#4363d8",
    4: "#000000", 5: "#f58231", 6: "#46f0f0", 7: "#f032e6", 8: "#000000"
};
export default function MachiningFeatureDisplay({ selectedFeatures }: { selectedFeatures: boolean[] }) {
    const [images, setImages] = useState<string[]>([]);

    useEffect(() => {
        const fetchImages = async () => {
            try {
                const response = await fetch("/api/machiningFeature");
                if (response.ok) {
                    const files = await response.json();

                    const sortedFiles = files.sort((a: string, b: string) => {
                        const numA = extractNumber(a);
                        const numB = extractNumber(b);
                        return numA - numB;
                    });

                    setImages(sortedFiles);
                } else {
                    console.error("Fehler beim Abrufen der MachiningFeatureTemplates");
                }
            } catch (error) {
                console.error("Netzwerkfehler:", error);
            }
        };

        void fetchImages();
    }, []);

    function extractNumber(fileName: string): number {
        const match = fileName.match(/\d+/);
        return match ? parseInt(match[0], 10) : 9999;
    }

    return (
        <Box
            sx={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fill, minmax(120px, 1fr))",
                gap: 2,
                justifyContent: "center",
                width: "100%",
                maxWidth: "1200px",
                marginTop: 2
            }}
        >
            {images.map((fileName, index) => {
                const isHighlighted = Boolean(selectedFeatures[index]);
                const backgroundColor = isHighlighted ? labelColors[index % Object.keys(labelColors).length] : "#787474";

                return (
                    <Box
                        key={index}
                        sx={{
                            width: 120,
                            height: 120,
                            display: "flex",
                            flexDirection: "column",
                            alignItems: "center",
                            justifyContent: "center",
                            border: "1px solid #ccc",
                            borderRadius: "10px",
                            padding: 1,
                            backgroundColor: backgroundColor,
                        }}
                    >
                        <img
                            src={`/machiningFeatureTemplates/${fileName}`}
                            alt={fileName}
                            width={80}
                            height={80}
                            style={{ objectFit: "contain" }}
                        />
                        <Typography variant="caption" sx={{ marginTop: 1, color: "white" }}>
                            {fileName.replace(".svg", "")}
                        </Typography>
                    </Box>
                );
            })}
        </Box>
    );
}
