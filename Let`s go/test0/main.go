package main

import (
	"fmt"
	"net/url"
	"os"
	"os/exec"

	"github.com/kennygrant/sanitize"
)

func main() {
	uri := "rtsp://10.25.144.106:554/live?camera=146&user=duansishengtims&pass=E0QjCAJLEHFC"
	URL, _ := url.Parse(uri)
	// fmt.Sprintf(URL)
	fmt.Println(URL.Hostname())
	fmt.Println(URL.Port())
	fmt.Println(sanitize.Path(URL.Path))
	fmt.Println(sanitize.Path(URL.RawQuery))
	path := sanitize.BaseName(fmt.Sprintf("%s-%s-%s-%s", URL.Hostname(), URL.Port(), sanitize.Path(URL.Path), sanitize.Path(URL.RawQuery)))
	fmt.Println(path)

	cmd := exec.Command(
		"ffmpeg",
		"-y",
		"-fflags",
		"nobuffer",
		"-rtsp_transport",
		"tcp",
		"-i",
		fmt.Sprintf("\"%s\"", uri),
		"-vsync",
		"0",
		"-copyts",
		"-vcodec",
		"copy",
		"-movflags",
		"frag_keyframe+empty_moov",
		"-an",
		"-hls_flags",
		"delete_segments+append_list",
		"-f",
		"hls",
		"-segment_list_flags",
		"live",
		"-hls_time",
		"1",
		"-hls_list_size",
		"3",
		"-hls_segment_filename",
		fmt.Sprintf("%s/%%d.ts", path),
		fmt.Sprintf("%s/index.m3u8", path),
	)
	fmt.Println(cmd.)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err := cmd.Run()
	if err != nil {
		fmt.Println(err)
	}
}
