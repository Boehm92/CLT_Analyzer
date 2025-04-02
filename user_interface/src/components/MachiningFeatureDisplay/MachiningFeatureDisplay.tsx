"use client";

import { useEffect, useState } from "react";
import { Box, Typography } from "@mui/material";
import Image from "next/image";

const labelColors: Record<number, string | null> = {
    0: "#ff0000",  1: "#ff7300", 2: "#ffbf00", 3: "#d4ff00", 4: "#66ff00",
    5: "#00ff33",  6: "#00ffbf", 7: "#00bfff", 8: "#0066ff", 9: "#0000ff",
    10: "#7300ff", 11: "#bf00ff", 12: "#ff00bf", 13: "#ff0066", 14: "#ff0033",
    15: "#800000", 16: "#804000", 17: "#808000", 18: "#408000", 19: "#008040",
    20: "#008080", 21: "#004080", 22: "#000080", 23: "#400080", 24: null
};

export default function MachiningFeatureDisplay({ selectedFeatures }: { selectedFeatures: boolean[] }) {
    const [images, setImages] = useState<string[]>([]);

    useEffect(() => {
        // 🔥 Asynchrone Funktion innerhalb des useEffect
        const fetchImages = async () => {
            try {
                const response = await fetch("/api/machiningFeature");
                if (response.ok) {
                    const files = await response.json();

                    // 🔹 Sortiere die Bilderliste nach Nummern
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

    // 🔹 Extrahiere die Nummer aus dem Dateinamen
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
                        <Image
                            src={`/machiningFeatureTemplates/${fileName}`}
                            alt={fileName}
                            width={80}
                            height={80}
                            style={{ objectFit: "contain" }} // ✅ Optimierte Bildgröße
                        />
                        <Typography variant="caption" sx={{ marginTop: 1, color: "white" }}>
                            {fileName.replace(".PNG", "").replace(".png", "")}
                        </Typography>
                    </Box>
                );
            })}
        </Box>
    );
}
