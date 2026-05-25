"use client";

import { Box, Typography } from "@mui/material";

export default function InfoBox({ combinedResponse }: { combinedResponse: { volume: number, body_center: number[], length: number, width: number, height: number, time: number } | null }) {

    const formatTime = (time: number | undefined | null) => {
        if (time === undefined || time === null || isNaN(time)) return "0 min 00 sek";
        const minutes = Math.floor(time);
        const seconds = Math.round((time - minutes) * 60);
        return `${minutes} min ${seconds.toString().padStart(2, "0")} sek`;
    };

    return (
        <Box
            sx={{
                width: "20vw",
                minWidth: "200px",
                height: "40vw",
                maxHeight: "400px",
                borderRadius: 2,
                bgcolor: "#787474",
                boxShadow: "3px 3px 10px rgba(0,0,0,0.2)",
                padding: 2,
                overflowY: "auto",
                display: "flex",
                flexDirection: "column",
                justifyContent: "flex-start",
                color: "white",
            }}
        >
            <Typography variant="h6" sx={{ fontWeight: "bold", marginBottom: 1 }}>
                ● Dimensions:
            </Typography>
            <Typography sx={{ marginLeft: 2 }}>
                • <b>Length:</b> {((combinedResponse?.length ?? 0) / 1000).toFixed(2)} m <br />
                • <b>Width:</b> {((combinedResponse?.width ?? 0) / 1000).toFixed(2)} m <br />
                • <b>Height:</b> {((combinedResponse?.height ?? 0) / 1000).toFixed(2)} m <br />
                • <b>Volume:</b> {((combinedResponse?.volume ?? 0) / 1_000_000_000).toFixed(2)} m³
            </Typography>

            <Typography variant="h6" sx={{ fontWeight: "bold", marginTop: 2 }}>
                ● Manufacturing Time:
            </Typography>
            <Typography sx={{ marginLeft: 2 }}>
                •  {formatTime(combinedResponse?.time)}
            </Typography>
        </Box>
    );
}
