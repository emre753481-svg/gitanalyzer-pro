#!/bin/bash
# GitAnalyzer Pro - Quick Start Script

set -e

echo "🚀 GitAnalyzer Pro - Quick Start"
echo "================================"
echo ""

# Check if .env exists
if [ ! -f backend/.env ]; then
    echo "⚠️  backend/.env dosyası bulunamadı!"
    echo ""
    echo "Lütfen backend/.env dosyası oluşturun:"
    echo ""
    echo "cat > backend/.env << 'EOF'"
    echo "GITHUB_TOKEN=your_github_token_here"
    echo "AI_PROVIDER=anthropic"
    echo "ANTHROPIC_API_KEY=your_anthropic_api_key_here"
    echo "OPENAI_API_KEY=your_openai_api_key_here"
    echo "PERPLEXITY_API_KEY=your_perplexity_api_key_here"
    echo "EOF"
    echo ""
    exit 1
fi

echo "✅ backend/.env dosyası bulundu"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker yüklü değil!"
    echo "Lütfen Docker'ı yükleyin: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✅ Docker bulundu"
echo ""

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose yüklü değil!"
    echo "Lütfen Docker Compose'u yükleyin: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker Compose bulundu"
echo ""

# Start services
echo "🔨 Docker containers başlatılıyor..."
docker-compose up -d

echo ""
echo "✅ Başarılı! GitAnalyzer Pro çalışıyor!"
echo ""
echo "📍 Erişim Noktaları:"
echo "   Frontend:  http://localhost"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "📊 Container durumunu kontrol et:"
echo "   docker-compose ps"
echo ""
echo "📋 Logları görüntüle:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Durdur:"
echo "   docker-compose down"
echo ""
echo "🎉 İyi çalışmalar!"
