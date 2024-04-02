package main

import (
	"bufio"
	"fmt"
	"math"
	"math/rand"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
	"time"
)

var (
	pa   = `N(\d{2})(\d{2})(\d{2}\.\d)E(\d{2})(\d{2})(\d{2}\.\d{1,3})`
	pb   = `N(\d{2})(\d{1,2}\.\d+)E(\d{2})(\d{1,2}\.\d{1,3})`
	pc_d = `N?(\d+\.\d+)E?(\d{2}\.\d+)`
)

func clearData(data string) string {
	// Заменяем запятые на точки
	data = strings.ReplaceAll(data, ",", ".")

	// Удаляем все символы, кроме цифр, точек, N и E
	// В регулярном выражении [^0-9.NE] означает "всё, кроме цифр, точек, N и E"
	reg := regexp.MustCompile(`[^0-9.NE]+`)
	data = reg.ReplaceAllString(data, "")

	return data
}
func selectScenario(pattern string, data string) (float64, float64) {
	var lat, lon float64
	re := regexp.MustCompile(pattern)
	matches := re.FindStringSubmatch(data)

	if matches == nil {
		return lat, lon
	}

	switch len(matches) {
	case 3:
		lat, _ = strconv.ParseFloat(matches[1], 64)
		lon, _ = strconv.ParseFloat(matches[2], 64)
	case 5:
		latDegrees, _ := strconv.ParseFloat(matches[1], 64)
		latMinutes, _ := strconv.ParseFloat(matches[2], 64)
		lonDegrees, _ := strconv.ParseFloat(matches[3], 64)
		lonMinutes, _ := strconv.ParseFloat(matches[4], 64)
		lat = latDegrees + latMinutes/60
		lon = lonDegrees + lonMinutes/60
	case 7:
		latDegrees, _ := strconv.ParseFloat(matches[1], 64)
		latMinutes, _ := strconv.ParseFloat(matches[2], 64)
		latSeconds, _ := strconv.ParseFloat(matches[3], 64)
		lonDegrees, _ := strconv.ParseFloat(matches[4], 64)
		lonMinutes, _ := strconv.ParseFloat(matches[5], 64)
		lonSeconds, _ := strconv.ParseFloat(matches[6], 64)
		lat = latDegrees + latMinutes/60 + latSeconds/3600
		lon = lonDegrees + lonMinutes/60 + lonSeconds/3600
	}

	return round(lat, 5), round(lon, 5)
}

func round(val float64, precision int) float64 {
	ratio := math.Pow(10, float64(precision))
	return math.Round(val*ratio) / ratio
}

func convertCoordinates(geoData string) (float64, float64) {
	geoData = clearData(geoData)
	var patterns = []string{pa, pb, pc_d}
	for _, pattern := range patterns {
		if regexp.MustCompile(pattern).MatchString(geoData) {
			return selectScenario(pattern, geoData)
		}
	}
	return 0, 0
}

func main() {
	rand.Seed(time.Now().UnixNano())

	executablePath, err := os.Executable()
	if err != nil {
		fmt.Println("Ошибка получения пути к исполняемому файлу:", err)
		return
	}

	executableDir := filepath.Dir(executablePath)
	savePathGpx := filepath.Join(executableDir, "coord_fixed.gpx")

	head := `<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<gpx xmlns="http://www.topografix.com/GPX/1/1" creator="MapSource 6.16.3" version="1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">

  <metadata>
    <link href="http://www.garmin.com">
      <text>Garmin International</text>
    </link>
    <time>2024-01-23T12:24:21Z</time>
    <bounds maxlat="56.092479145154357" maxlon="55.898553002625704" minlat="53.633718425408006" minlon="51.073859967291355"/>
  </metadata>`
	tail := `
</gpx>`

	filePath := filepath.Join(executableDir, "file.txt")
	file, err := os.Open(filePath)
	if err != nil {
		fmt.Println("Ошибка при открытии файла с координатами:", err)
		return
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	output := ""
	height := getInputHeight()
	for i := 0; scanner.Scan(); i++ {
		line := scanner.Text()
		lat, lon := convertCoordinates(line)
		output += fmt.Sprintf(`  <wpt lat="%f" lon="%f">
    <ele>%d</ele>
    <time>2024-01-16T12:56:09Z</time>
    <name>%03d</name>
    <cmt>30-APR-04 0:57:35</cmt>
    <desc>30-APR-04 0:57:35</desc>
    <sym>Flag, Green</sym>
    <extensions>
      <gpxx:WaypointExtension xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3">
        <gpxx:DisplayMode>SymbolAndName</gpxx:DisplayMode>
      </gpxx:WaypointExtension>
    </extensions>
  </wpt>
`, lat, lon, height, i+1)
	}

	if err := scanner.Err(); err != nil {
		fmt.Println("Ошибка при сканировании файла:", err)
		return
	}

	output = head + output + tail

	gpxFile, err := os.Create(savePathGpx)
	if err != nil {
		fmt.Println("Ошибка при создании файла GPX:", err)
		return
	}
	defer gpxFile.Close()

	if _, err := gpxFile.WriteString(output); err != nil {
		fmt.Println("Ошибка при записи файла GPX:", err)
	}
}

func getInputHeight() int {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Введите высоту (оставить пустым для назаначения случайного значения): ")
	heightStr, _ := reader.ReadString('\n')
	heightStr = strings.TrimSpace(heightStr)
	if heightStr == "" {
		return rand.Intn(50) + 45
	}
	height, err := strconv.Atoi(heightStr)
	if err != nil {
		fmt.Println("Ошибка при получении высоты:", err)
		return getInputHeight()
	}
	return height
}
