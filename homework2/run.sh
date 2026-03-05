#!/usr/bin/env bash
cd /home/student/cs4300/homework2
source myenv/bin/activate
python manage.py migrate --run-syncdb 2>/dev/null

echo ""
echo "========================================="
echo "  Fandangle Movie Booking"
echo "  http://localhost:3000/movies/"
echo "========================================="
echo ""

# Start server in background, wait for it, then open browser
python manage.py runserver 0.0.0.0:3000 &
SERVER_PID=$!

# Wait for server to be ready
sleep 3
xdg-open http://localhost:3000/movies/ 2>/dev/null

# Bring server back to foreground
wait $SERVER_PID
