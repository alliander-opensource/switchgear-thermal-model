/*
  SPDX-FileCopyrightText: Contributors to the Switchgear Thermal Model project

  SPDX-License-Identifier: MPL-2.0
*/

document$.subscribe(({ body }) => {
    renderMathInElement(body, {
        delimiters: [
            { left: "$$", right: "$$", display: true },
            { left: "$", right: "$", display: false },
            { left: String.raw`\(`, right: String.raw`\)`, display: false },
            { left: String.raw`\[`, right: String.raw`\]`, display: true }
        ],
    })
})