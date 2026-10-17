def style_figure(fig):
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
    )

    return fig
