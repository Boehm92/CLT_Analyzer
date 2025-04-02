// 🔥 Datei-Verarbeitung: Hochladen, Auswahl und REST-Aufruf
import { blobToBase64, sendToRestAPIMFS, sendToRestAPIMFR, sendToRestAPIMTE } from "./restService";
import React from "react";

// Datei Typdefinition
export interface STLFile {
    name: string;
    url: string;
    file: File;
}

export const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>,
    setFiles: React.Dispatch<React.SetStateAction<STLFile[]>>,
    setFileUrl: React.Dispatch<React.SetStateAction<string | null>>,
    setOpen: React.Dispatch<React.SetStateAction<boolean>>
) => {
    const file = event.target.files?.[0];
    if (file) {
        const url = URL.createObjectURL(file);
        const newFile: STLFile = { name: file.name, url, file };
        setFiles((prev) => [...prev, newFile]);
        setFileUrl(url);
        setOpen(false);
        console.log("✅ Datei hochgeladen:", newFile.name);
    } else {
        console.error("❌ Keine Datei ausgewählt");
    }
};

export const handleSelectFile = async (
    fileUrl: string,
    setFileUrl: React.Dispatch<React.SetStateAction<string | null>>,
    setFeatures: React.Dispatch<React.SetStateAction<number[][]>>,
    setPredictedLabels: React.Dispatch<React.SetStateAction<number[]>>,
    setMfrFeatures: React.Dispatch<React.SetStateAction<number[]>>,
    setCombinedResponse: React.Dispatch<React.SetStateAction<{ volume: number, body_center: number[], length: number, width: number, height: number, time: number } | null>>
) => {
    setFileUrl(fileUrl);
    console.log("🚀 Datei ausgewählt:", fileUrl);

    try {
        // Datei laden
        const response = await fetch(fileUrl);
        const blob = await response.blob();

        // Blob in Base64 konvertieren
        const base64File = await blobToBase64(blob);

        if (base64File) {
            const labelData = await sendToRestAPIMFS(base64File);
            if (labelData) {
                setFeatures(labelData.features);
                setPredictedLabels(labelData.predicted_labels);
            } else {
                console.error("❌ Keine Labeldaten erhalten");
            }

            const mfrData = await sendToRestAPIMFR(base64File);
            setMfrFeatures(mfrData);

            const combinedResponse = await sendToRestAPIMTE(base64File);
            if (combinedResponse) {
                setCombinedResponse(combinedResponse);
                console.log("🚀 Combined Response:", combinedResponse);
            } else {
                console.error("❌ Keine kombinierten Daten erhalten");
            }

        } else {
            console.error("❌ Fehler beim Konvertieren der Datei in Base64");
        }
    } catch (error) {
        console.error("❌ Fehler beim Laden der Datei für den REST-Request", error);
    }
};