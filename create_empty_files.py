import os

def create_directory_structure():
    # 创建主目录
    main_dir = "[VCB-Studio] Mahou Tsukai no Yome [Ma10p_1080p]"
    os.makedirs(main_dir, exist_ok=True)
    
    # 创建SPs子目录
    sps_dir = os.path.join(main_dir, "SPs")
    os.makedirs(sps_dir, exist_ok=True)
    
    # SPs目录中的文件
    sp_files = [
        "[VCB-Studio] Mahou Tsukai no Yome Hoshi Matsu Hito [Event01][Ma10p_1080p][x265_aac].mkv",
        "[VCB-Studio] Mahou Tsukai no Yome Hoshi Matsu Hito [Event02][Ma10p_1080p][x265_aac].mkv",
        "[VCB-Studio] Mahou Tsukai no Yome Hoshi Matsu Hito [Event03][Ma10p_1080p][x265_aac].mkv",
        "[VCB-Studio] Mahou Tsukai no Yome Hoshi Matsu Hito [Trailer][Ma10p_1080p][x265_flac].mkv",
        "[VCB-Studio] Mahou Tsukai no Yome [Event01][Ma10p_1080p][x265_aac].mkv",
        "[VCB-Studio] Mahou Tsukai no Yome [Event02][Ma10p_1080p][x265_aac].mkv",
        "[VCB-Studio] Mahou Tsukai no Yome [Location Hunting 01][Ma10p_1080p][x265_2aac].mkv",
        "[VCB-Studio] Mahou Tsukai no Yome [Location Hunting 02][Ma10p_1080p][x265_2aac].mkv",
        "[VCB-Studio] Mahou Tsukai no Yome [Menu01].png",
        "[VCB-Studio] Mahou Tsukai no Yome [Menu02].png",
        "[VCB-Studio] Mahou Tsukai no Yome [Menu03].png",
        "[VCB-Studio] Mahou Tsukai no Yome [Menu04].png",
        "[VCB-Studio] Mahou Tsukai no Yome [NCED01][Ma10p_1080p][x265_flac].mkv",
        "[VCB-Studio] Mahou Tsukai no Yome [NCED02][Ma10p_1080p][x265_flac].mkv",
        "[VCB-Studio] Mahou Tsukai no Yome [NCOP01][Ma10p_1080p][x265_flac].mkv",
        "[VCB-Studio] Mahou Tsukai no Yome [NCOP02][Ma10p_1080p][x265_flac].mkv",
        "[VCB-Studio] Mahou Tsukai no Yome [NCOP03][Ma10p_1080p][x265_flac].mkv",
        "[VCB-Studio] Mahou Tsukai no Yome [PV01][Ma10p_1080p][x265_flac].mkv",
        "[VCB-Studio] Mahou Tsukai no Yome [PV02][Ma10p_1080p][x265_flac].mkv",
        "[VCB-Studio] Mahou Tsukai no Yome [PV03][Ma10p_1080p][x265_flac].mkv",
        "[VCB-Studio] Mahou Tsukai no Yome [PV04][Ma10p_1080p][x265_flac].mkv",
        "[VCB-Studio] Mahou Tsukai no Yome [SP][Ma10p_1080p][x265_flac].mkv"
    ]
    
    # 主目录中的文件
    main_files = [
        "[VCB-Studio] Mahou Tsukai no Yome Hoshi Matsu Hito [01][Ma10p_1080p][x265_flac].mkv",
        "[VCB-Studio] Mahou Tsukai no Yome Hoshi Matsu Hito [02][Ma10p_1080p][x265_flac].mkv",
        "[VCB-Studio] Mahou Tsukai no Yome Hoshi Matsu Hito [03][Ma10p_1080p][x265_flac].mkv"
    ]
    
    # 添加主系列剧集
    for i in range(1, 25):
        suffix = "_aac" if i in [1, 2, 22, 24] else ""
        main_files.append(f"[VCB-Studio] Mahou Tsukai no Yome [{i:02d}][Ma10p_1080p][x265_flac{suffix}].mkv")
    
    # 创建SPs目录中的空文件
    for file in sp_files:
        with open(os.path.join(sps_dir, file), 'w') as f:
            pass
    
    # 创建主目录中的空文件
    for file in main_files:
        with open(os.path.join(main_dir, file), 'w') as f:
            pass

if __name__ == "__main__":
    create_directory_structure()
    print("目录结构和空文件已创建完成！") 