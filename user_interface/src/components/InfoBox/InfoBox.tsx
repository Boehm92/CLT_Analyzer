"use client";

import { Box, Typography } from "@mui/material";

export default function InfoBox({ combinedResponse }: { combinedResponse: { volume: number, body_center: number[], length: number, width: number, height: number, time: number } | null }) {
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
                justifyContent: "center",
                color: "white",
            }}
        >
            <Typography variant="h6" sx={{ fontWeight: "bold", marginBottom: 1 }}>
                ● Dimensions:
            </Typography>
            <Typography sx={{ marginLeft: 2 }}>
                • <b>Length:</b> {(combinedResponse?.length ? (combinedResponse.length / 1000).toFixed(3) : "0.000")} m <br />
                • <b>Width:</b> {(combinedResponse?.width ? (combinedResponse.width / 1000).toFixed(3) : "0.000")} m <br />
                • <b>Height:</b> {(combinedResponse?.height ? (combinedResponse.height / 1000).toFixed(3) : "0.000")} m <br />

                • <b>Volume:</b> {(combinedResponse?.volume ? (combinedResponse.volume / 1_000_000_000).toFixed(3) : "0.000000000")} m³
            </Typography>

            <Typography variant="h6" sx={{ fontWeight: "bold", marginTop: 2 }}>
                ● Center of Gravity:
            </Typography>
            <Typography sx={{ marginLeft: 2 }}>
                • <b>X:</b> {combinedResponse?.body_center?.[0] !== undefined ? (combinedResponse.body_center[0] / 1000).toFixed(3) : "0.000"} m <br />
                • <b>Y:</b> {combinedResponse?.body_center?.[1] !== undefined ? (combinedResponse.body_center[1] / 1000).toFixed(3) : "0.000"} m <br />
                • <b>Z:</b> {combinedResponse?.body_center?.[2] !== undefined ? (combinedResponse.body_center[2] / 1000).toFixed(3) : "0.000"} m <br />

            </Typography>

            <Typography variant="h6" sx={{ fontWeight: "bold", marginTop: 2 }}>
                ● Production:
            </Typography>
            <Typography sx={{ marginLeft: 2 }}>
                • <b>Post-processing:</b> {combinedResponse?.time?.toFixed(2) || "0.00"} min
            </Typography>
        </Box>
    );
}
