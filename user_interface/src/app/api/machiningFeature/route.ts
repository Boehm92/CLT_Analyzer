// api/machiningFeature.ts
import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function GET() {
    try {
        const templatesDir = path.join(process.cwd(), "public/machiningFeatureTemplates");

        if (!fs.existsSync(templatesDir)) {
            console.error("📁 Fehler: Der Ordner machiningFeatureTemplates existiert nicht.");
            return NextResponse.json({ error: "Ordner existiert nicht" }, { status: 404 });
        }

        // Ändere Filter von .png auf .svg
        const files = fs.readdirSync(templatesDir).filter(file => file.toLowerCase().endsWith(".svg"));

        console.log("📄 Gefundene SVG-Dateien:", files);

        return NextResponse.json(files);
    } catch (error) {
        console.error("❌ Fehler beim Laden der SVG-Dateien:", error);
        return NextResponse.json({ error: "Serverfehler" }, { status: 500 });
    }
}
