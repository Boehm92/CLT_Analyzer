export const sendToRestAPIMFR = async (base64File: string): Promise<number[]> => {
    try {
        const response = await fetch("http://127.0.0.1:5002/processstlmodel", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ stl_base64: base64File }),
        });

        if (!response.ok) {
            console.error("❌ REST API Fehler (MFR):", response.status);
            return [];
        }

        const result = await response.json();
        console.log("🚀 MFR REST API Response:", result);

        if (Array.isArray(result) && Array.isArray(result[0])) {
            return result[0];
        } else {
            return result;
        }
    } catch (error) {
        console.error("❌ Netzwerkfehler (MFR)", error);
        return [];
    }
};

export const sendToRestAPIMFS = async (base64File: string): Promise<{ features: number[][], predicted_labels: number[] } | null> => {
    try {
        const response = await fetch("http://127.0.0.1:5001/processstlmodel", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ stl_base64: base64File }),
        });

        if (!response.ok) {
            console.error("❌ REST API Fehler:", response.status);
            return null;
        }

        const result = await response.json();
        console.log("🚀 REST API Response:", result);

        if (result.features && result.predicted_labels) {
            return {
                features: result.features,
                predicted_labels: result.predicted_labels
            };
        } else {
            console.error("❌ Unerwartetes Ergebnisformat");
            return null;
        }
    } catch (error) {
        console.error("❌ Netzwerkfehler", error);
        return null;
    }
};

export const sendToRestAPIMTE = async (base64File: string): Promise<{ volume: number, body_center: number[], length: number, width: number, height: number, time: number } | null> => {
    try {
        const response = await fetch("http://127.0.0.1:5003/processstlmodel", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ stl_base64: base64File }),
        });

        if (!response.ok) {
            console.error("❌ REST API Fehler:", response.status);
            return null;
        }

        const result = await response.json();
        console.log("🚀 REST API Response:", result);

        if (result.volume !== undefined && result.body_center && result.length !== undefined && result.width !== undefined && result.height !== undefined && result.time !== undefined) {
            return {
                volume: result.volume,
                body_center: result.body_center,
                length: result.length,
                width: result.width,
                height: result.height,
                time: result.time
            };
        } else {
            console.error("❌ Unerwartetes Ergebnisformat");
            return null;
        }
    } catch (error) {
        console.error("❌ Netzwerkfehler", error);
        return null;
    }
};

export const blobToBase64 = (blob: Blob): Promise<string | null> => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => {
            const base64File = reader.result?.toString().split(",")[1] || null;
            resolve(base64File);
        };
        reader.onerror = reject;
        reader.readAsDataURL(blob);
    });
};
