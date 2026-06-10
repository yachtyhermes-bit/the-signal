export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const key = url.pathname.slice(1); // remove leading /
    
    if (!key || !key.endsWith('.mp3')) {
      return new Response('Not Found', { status: 404 });
    }
    
    const object = await env.AUDIO_BUCKET.get(key);
    if (!object) {
      return new Response('Not Found', { status: 404 });
    }
    
    return new Response(object.body, {
      headers: {
        'Content-Type': 'audio/mpeg',
        'Cache-Control': 'public, max-age=31536000, immutable',
        'Accept-Ranges': 'bytes',
        'Content-Length': object.size,
      },
    });
  },
};
