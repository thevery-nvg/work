package main

import (
	"encoding/xml"
	"fmt"
	"math"
	"os"
	"strconv"
)

// Структура для хранения данных из XML
type Wpt struct {
	XMLName xml.Name `xml:"gpx"`
	Points  []Point  `xml:"wpt"`
}

type Point struct {
	XMLName xml.Name `xml:"wpt"`
	Lat     string   `xml:"lat,attr"`
	Lon     string   `xml:"lon,attr"`
	Name    string   `xml:"name"`
}

func crossProductZ(x1, y1, x2, y2 float64) float64 {
	return x1*y2 - x2*y1
}

func rotationDirection(latA, lonA, latB, lonB, latC, lonC float64) string {
	vectorAB := [2]float64{lonB - lonA, latB - latA}
	vectorBC := [2]float64{lonC - lonB, latC - latB}

	crossProduct := crossProductZ(vectorAB[0], vectorAB[1], vectorBC[0], vectorBC[1])

	if crossProduct > 0 {
		return "Налево"
	} else if crossProduct < 0 {
		return "Направо"
	} else {
		return "На одной прямой"
	}
}

func degreesToRadians(degrees float64) float64 {
	return degrees * (math.Pi / 180)
}

func angleBetweenPoints(latA, lonA, latB, lonB, latC, lonC float64) float64 {
	// Радиус Земли в километрах
	const EarthRadius = 6371.0

	// Преобразование градусов в радианы
	latARad := degreesToRadians(latA)
	latBRad := degreesToRadians(latB)

	// Вычисление векторов
	vectorAB := [2]float64{(lonB - lonA) * math.Cos(latARad), latB - latA}
	vectorBC := [2]float64{(lonC - lonB) * math.Cos(latBRad), latC - latB}

	// Скалярное произведение
	dotProduct := vectorAB[0]*vectorBC[0] + vectorAB[1]*vectorBC[1]

	// Длины векторов
	lengthAB := math.Sqrt(math.Pow(vectorAB[0], 2) + math.Pow(vectorAB[1], 2))
	lengthBC := math.Sqrt(math.Pow(vectorBC[0], 2) + math.Pow(vectorBC[1], 2))

	// Вычисление угла в радианах
	angleRad := math.Acos(dotProduct / (lengthAB * lengthBC))

	// Преобразование радиан в градусы
	angleDeg := angleRad * (180 / math.Pi)

	return angleDeg
}

func main() {
	var x string
	var filePath string

	if len(os.Args) > 1 {
		filePath = os.Args[1]
	} else {
		filePath = "data.gpx"
	}
	xmlFile, err := os.Open(filePath)
	if err != nil {
		fmt.Println("Ошибка открытия файла:", err)
		return
	}
	defer xmlFile.Close()
	var gpx Wpt
	err = xml.NewDecoder(xmlFile).Decode(&gpx)
	if err != nil {
		fmt.Println("Ошибка декодирования XML:", err)
		return
	}
	fmt.Println("Углы между точками:")
	fmt.Println("1 - 0.00°")
	for i := 0; i < len(gpx.Points)-2; i++ {
		pointA := gpx.Points[i]
		pointB := gpx.Points[i+1]
		pointC := gpx.Points[i+2]
		latA, _ := strconv.ParseFloat(pointA.Lat, 64)
		lonA, _ := strconv.ParseFloat(pointA.Lon, 64)
		latB, _ := strconv.ParseFloat(pointB.Lat, 64)
		lonB, _ := strconv.ParseFloat(pointB.Lon, 64)
		latC, _ := strconv.ParseFloat(pointC.Lat, 64)
		lonC, _ := strconv.ParseFloat(pointC.Lon, 64)
		angle := angleBetweenPoints(latA, lonA, latB, lonB, latC, lonC)
		direction := rotationDirection(latA, lonA, latB, lonB, latC, lonC)
		fmt.Printf("%d - %.2f° (%s)\n", i+2, angle, direction)
	}

	fmt.Println("Нажмите Enter чтобы закрыть окно...")
	fmt.Scanln(&x)
	fmt.Print(x)
}
