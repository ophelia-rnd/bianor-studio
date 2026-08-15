def style_figure(fig, colorscale="plasma"):
    fig.update_layout(
        # Canvas Transparency & Dark Palette
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            size=12,
            color="#94A3B8"
        ),

        # Compact Margins
        margin=dict(l=20, r=20, t=50, b=20),

        # Subtle, Minimal Axes
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor="#334155",
            tickcolor="#334155",
            zeroline=False,
            tickfont=dict(color="#64748B")
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#1E293B",
            showline=False,
            zeroline=False,
            tickfont=dict(color="#64748B")
        ),

        # Sleek Legend & Colorbar
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#94A3B8")
        )
    )

    # Compact, Slim Colorbars (if heatmap/2D plot)
    fig.update_coloraxes(
        colorscale=colorscale,
        colorbar=dict(
            len=1,
            thickness=30,
            outlinewidth=0,
            tickfont=dict(color="#64748B", size=12),
            title=dict(font=dict(color="#94A3B8", size=11))
        )
    )

    return fig
