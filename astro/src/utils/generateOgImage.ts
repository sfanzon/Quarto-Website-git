import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import satori from 'satori';
import { html } from 'satori-html';
import { Resvg } from '@resvg/resvg-js';
import { SITE_TITLE } from '../consts';

export async function generateOgImage(title: string, subtitle: string) {
    const [fontDataRegular, fontDataBold] = await Promise.all([
        readFile(resolve(process.cwd(), 'public/fonts/atkinson-regular.woff')),
        readFile(resolve(process.cwd(), 'public/fonts/atkinson-bold.woff'))
    ]);

    const markup = html`
        <div style="background-color: #0f172a; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; position: relative; font-family: 'Atkinson';">
            
            <div style="display: flex; position: absolute; top: -150px; right: -50px; width: 600px; height: 600px; background-image: linear-gradient(135deg, rgba(56, 189, 248, 0.4), rgba(49, 46, 129, 0)); border-radius: 50%;"></div>
            <div style="display: flex; position: absolute; bottom: -150px; left: -50px; width: 600px; height: 600px; background-image: linear-gradient(45deg, rgba(167, 139, 250, 0.4), rgba(88, 28, 135, 0)); border-radius: 50%;"></div>

            <div style="display: flex; flex-direction: column; justify-content: space-between; padding: 80px; width: 100%; height: 100%;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; width: 100%;">
                    <div style="display: flex; align-items: center; padding: 12px 24px; background-color: rgba(255, 255, 255, 0.1); border-radius: 999px; border: 1px solid rgba(255, 255, 255, 0.2);">
                        <span style="color: #ffffff; font-size: 24px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">
                            ${subtitle}
                        </span>
                    </div>
                </div>

                <div style="display: flex; flex-direction: column; gap: 24px; margin-bottom: 20px;">
                    <div style="display: flex; color: #ffffff; font-size: 84px; font-weight: 700; line-height: 1.1; letter-spacing: -0.02em; margin: 0; max-width: 900px; overflow: hidden; max-height: 280px;">
                        ${title}
                    </div>
                </div>

                <div style="display: flex; justify-content: space-between; align-items: flex-end; width: 100%;">
                    <div style="display: flex; flex-direction: column; gap: 8px;">
                        <span style="color: #cbd5e1; font-size: 32px; font-weight: 700;">${SITE_TITLE}</span>
                    </div>
                    <div style="display: flex; align-items: center; justify-content: center; width: 80px; height: 80px; background-color: #ffffff; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2);">
                        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                            <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                        </svg>
                    </div>
                </div>
            </div>
        </div>
    `;

    const svg = await satori(markup, {
        width: 1200,
        height: 630,
        fonts: [
            { name: "Atkinson", data: fontDataRegular, weight: 400, style: "normal" },
            { name: "Atkinson", data: fontDataBold, weight: 700, style: "normal" }
        ],
    });

    const resvg = new Resvg(svg);
    const pngData = resvg.render();
    return new Uint8Array(pngData.asPng());
}
