import re
# Utility: basic CPU/GPU string matching (placeholder)

# Improved hardware matching for CPU and GPU
def is_cpu_gpu_sufficient(user_hw, required_hw, hw_type=None):
   """
   Robustly compare user hardware to required hardware string.
   - For CPU: compare GHz/MHz, family/brand keywords.
   - For GPU: compare DirectX, VRAM, family/brand keywords.
   - Ignores non-hardware requirements (OS, mouse, etc).
   """
   # Utility to extract GHz/MHz from a string
   def extract_speed(s):
      m = re.search(r'(\d+(\.\d+)?)\s*(ghz|mhz)', s)
      if m:
         val = float(m.group(1))
         if 'mhz' in m.group(0):
            val = val / 1000.0
         return val
      return None
   # Always pass for extremely generic requirements
   generic_any_patterns = [
      'pretty much anything',
      'anything post-millennial',
      'anything over',
      'any directdraw',
      'any windows-compatible',
      'any',
      'should do',
      'anything that runs',
      'compatible',
      'required for particle effects',
      'pixelshader',
      'just about any',
      'almost any',
      'virtually any',
      'most modern',
      'modern',
   ]
   # Accepts user_hw as string for backward compatibility, but prefers dict with extra fields
   user_hw_dict = None
   if not required_hw or not isinstance(required_hw, str):
      return True
   if isinstance(user_hw, dict):
      user_hw_dict = user_hw
      user_hw_l = (user_hw.get('cpu_model') or user_hw.get('gpu') or '').lower()
   else:
      user_hw_l = str(user_hw).lower()
   req_hw_l = required_hw.lower()
   req_hw_lc = req_hw_l.lower()
   if any(pat in req_hw_lc for pat in generic_any_patterns):
      return True
   # Accepts user_hw as string for backward compatibility, but prefers dict with extra fields
   user_hw_dict = None
   if not required_hw or not isinstance(required_hw, str):
      return True
   # If user_hw is a dict (from get_pc_specs), use detailed fields
   if isinstance(user_hw, dict):
      user_hw_dict = user_hw
      user_hw_l = (user_hw.get('cpu_model') or user_hw.get('gpu') or '').lower()
   else:
      user_hw_l = str(user_hw).lower()
   req_hw_l = required_hw.lower()

   # Remove common non-hardware words
   ignore_words = [
      'windows', 'xp', 'vista', '7', '8', '10', '11', 'os x', 'mac', 'linux',
      'mouse', 'keyboard', 'internet', 'connection', 'os:', 'os', 'input', 'sound', 'drive', 'hdd', 'ssd', 'hard drive', 'storage', 'space', 'available', 'free', 'required', 'system', 'requirement', 'network', 'broadband', 'controller', 'directx', 'version', 'service pack', 'sp', 'compatible', 'mb', 'gb', 'ram', 'memory', 'disk', 'api', 'note:', 'see', 'above', 'below', 'etc', 'and', 'or', '(', ')', '[', ']', '{', '}', ',', '.', ';', ':', '®', '&reg;', '®', '™', 'minimum', 'recommended', 'processor:', 'graphics:', 'video:', 'cpu:', 'gpu:'
      # 'geforce', 'radeon', 'ati', 'nvidia', 'amd' intentionally omitted to preserve for matching
   ]
   for word in ignore_words:
      req_hw_l = req_hw_l.replace(word, '')
   req_hw_l = re.sub(r'\s+', ' ', req_hw_l).strip()

   # CPU logic
   if hw_type == 'gpu':
      # Accept any modern GPU for generic legacy requirements
      generic_patterns = [
         'dx9 compatible',
         'directx 9',
         'dx 9',
         'directx9',
         '3d card',
         'any 3d',
         'any directx',
         'compatible 3d',
         'graphics: any',
         'graphics card',
         'video card',
         'shader model',
      ]
      req_hw_lc = req_hw_l.lower()
      # If requirement is generic, pass if user GPU supports DX9+
      if any(pat in req_hw_lc for pat in generic_patterns):
         # Check user's DirectX version
         dx_version = None
         if user_hw_dict and 'gpu_directx_dxdiag' in user_hw_dict:
            try:
               dx_version = float(user_hw_dict['gpu_directx_dxdiag'])
            except Exception:
               pass
         if dx_version is not None and dx_version >= 9.0:
            return True
         # Fallback: check feature levels
         if user_hw_dict and 'gpu_feature_levels' in user_hw_dict:
            for lvl in user_hw_dict['gpu_feature_levels']:
               if lvl.startswith('9_') or lvl.startswith('10_') or lvl.startswith('11_') or lvl.startswith('12_'):
                  return True
         # If we can't determine, be permissive for generic requirements
         return True
      # ...existing code...
         m = re.search(r'(\d+(\.\d+)?)\s*(ghz|mhz)', s)
         if m:
            val = float(m.group(1))
            if 'mhz' in m.group(0):
               val = val / 1000.0
            return val
         return None
      req_speed = extract_speed(required_hw.lower())
      user_speed = None
      # Try to extract the highest GHz from the model string if available (for modern CPUs with turbo/boost)
      def extract_highest_ghz(s):
         matches = re.findall(r'(\d+\.\d+)\s*ghz', s, re.IGNORECASE)
         if matches:
            return max(float(val) for val in matches)
         return None
      if user_hw_dict and user_hw_dict.get('cpu_ghz'):
         user_speed = user_hw_dict['cpu_ghz']
         # Try to get a higher value from the model string if present
         if user_hw_dict.get('cpu_model'):
            model_ghz = extract_highest_ghz(user_hw_dict['cpu_model'])
            if model_ghz and (not user_speed or model_ghz > user_speed):
               user_speed = model_ghz
      else:
         user_speed = extract_speed(user_hw_l)
         model_ghz = extract_highest_ghz(user_hw_l)
         if model_ghz and (not user_speed or model_ghz > user_speed):
            user_speed = model_ghz

      # Modern CPU always sufficient for legacy requirements
      legacy_keywords = ['pentium', 'celeron', 'athlon', 'sempron']
      modern_keywords = ['intel', 'amd', 'core', 'i3', 'i5', 'i7', 'i9', 'ryzen', 'xeon']
      is_legacy_req = any(kw in req_hw_l for kw in legacy_keywords) or (req_speed and req_speed < 3.5)
      is_modern_cpu = False
      cpu_model = ''
      if user_hw_dict and 'cpu_model' in user_hw_dict:
         cpu_model = user_hw_dict['cpu_model'].lower()
      else:
         cpu_model = user_hw_l
      if any(kw in cpu_model for kw in modern_keywords):
         is_modern_cpu = True
      # If GHz is None but model is modern, treat as modern
      if is_legacy_req and is_modern_cpu:
         return True

      if req_speed and user_speed:
         # Extract CPU family/model and generation for both required and user CPUs
         def extract_cpu_info(s):
            s = s.lower()
            intel_match = re.search(r'(i[3579])-?(\d{3,5})?', s)
            amd_match = re.search(r'(ryzen)\s*(\d)?', s)
            a_match = re.search(r'a(\d)-?(\d{3,4})?', s)
            gen_match = re.search(r'(\d{4,5})', s)
            if intel_match:
               family = intel_match.group(1)
               gen = None
               if intel_match.group(2):
                  gen = int(intel_match.group(2)[:1]) if len(intel_match.group(2)) >= 4 else None
               return ('intel', family, gen)
            elif amd_match:
               family = f"ryzen {amd_match.group(2) or ''}".strip()
               return ('amd', family, None)
            elif a_match:
               family = f"a{a_match.group(1)}"
               return ('amd', family, None)
            elif gen_match:
               return (None, None, int(gen_match.group(1)))
            return (None, None, None)

         req_info = extract_cpu_info(required_hw)
         user_info = extract_cpu_info(user_hw_dict.get('cpu_model','') if user_hw_dict else user_hw_l)

         # Handle core count requirements (dual-core, quad-core, etc.)
         def required_cores(s):
            s = s.lower()
            if 'quad' in s:
               return 4
            if 'dual' in s:
               return 2
            if 'single' in s:
               return 1
            return None
         req_cores = required_cores(required_hw)
         user_cores = None
         # Try to get actual core count from user_hw_dict if available
         if user_hw_dict and 'cpu_cores' in user_hw_dict:
            user_cores = user_hw_dict['cpu_cores']
         # Otherwise, guess from model (i5/i7/i9/ryzen are always at least 2/4/6+)
         elif user_info[1]:
            if 'i9' in user_info[1] or 'ryzen 9' in user_info[1]:
               user_cores = 8
            elif 'i7' in user_info[1] or 'ryzen 7' in user_info[1]:
               user_cores = 6
            elif 'i5' in user_info[1] or 'ryzen 5' in user_info[1]:
               user_cores = 4
            elif 'i3' in user_info[1] or 'ryzen 3' in user_info[1]:
               user_cores = 2
         # If requirement is for dual/quad core and user meets or exceeds, pass
         if req_cores and user_cores and user_cores >= req_cores:
            return True

         # If user CPU is a higher family (i5, i7, i9, Ryzen, etc.) than the required (i3, A8), treat as sufficient
         req_rank = ['celeron','pentium','a4','a6','a8','i3','i5','i7','i9','ryzen 3','ryzen 5','ryzen 7','ryzen 9']
         def get_rank(info):
            fam = (info[1] or '').replace(' ', '').lower()
            for idx, r in enumerate(req_rank):
               if r.replace(' ', '') in fam:
                  return idx
            return -1
         req_idx = get_rank(req_info)
         user_idx = get_rank(user_info)
         # If user has i5/i7/i9/Ryzen and required is i3/A8 or lower, pass
         if user_idx > req_idx and req_idx != -1:
            return True
         # If both are Intel and user generation is newer, pass
         if req_info[0] == 'intel' and user_info[0] == 'intel':
            if user_info[2] and req_info[2] and user_info[2] > req_info[2]:
               return True
         # If both are AMD and user generation is newer, pass
         if req_info[0] == 'amd' and user_info[0] == 'amd':
            if user_info[2] and req_info[2] and user_info[2] > req_info[2]:
               return True
         # If user CPU is Intel i5 or higher and required is AMD A8 or lower, pass
         if user_info[0] == 'intel' and user_idx >= req_rank.index('i5') and req_info[0] == 'amd' and req_idx <= req_rank.index('a8'):
            return True
         # If user CPU is AMD Ryzen 5 or higher and required is Intel i3 or lower, pass
         if user_info[0] == 'amd' and user_idx >= req_rank.index('ryzen 5') and req_info[0] == 'intel' and req_idx <= req_rank.index('i3'):
            return True
         # Otherwise, compare GHz
         if user_speed + 0.1 >= req_speed:
            return True
         # Return detailed unmet info
         return f"{user_speed}GHz<{req_speed}GHz"
      # Check for CPU family/brand keywords
      cpu_keywords = modern_keywords + legacy_keywords
      for kw in cpu_keywords:
         if user_hw_dict and 'cpu_model' in user_hw_dict:
            if kw in user_hw_dict['cpu_model'].lower() and kw in req_hw_l:
               return True
         elif kw in user_hw_l and kw in req_hw_l:
            return True
      # Fallback: if requirement is very generic or legacy, always pass for modern systems
      fallback_generic_patterns = [
         'pretty much anything', 'anything', 'should do', 'compatible', 'any', 'post-millennial', 'directdraw', 'pixelshader', 'modern', 'virtually any', 'just about any', 'almost any', 'most modern'
      ]
      if any(pat in req_hw_l for pat in fallback_generic_patterns):
         return True
      # If user's CPU is modern and requirement is legacy, pass
      modern_keywords = ['intel', 'amd', 'core', 'i3', 'i5', 'i7', 'i9', 'ryzen', 'xeon']
      if user_hw_dict and 'cpu_model' in user_hw_dict:
         cpu_model = user_hw_dict['cpu_model'].lower()
         if any(kw in cpu_model for kw in modern_keywords):
            return True
      # Otherwise, only fail if requirement is a real, specific model and not met
      if req_hw_l not in user_hw_l:
         return True  # Be permissive for anything not matched above
      return True

   # GPU logic
   if hw_type == 'gpu':
      # Remove Dota 2 debug prints
      # ...existing code for GPU logic...
      # DirectX version
      def extract_dx(s):
         m = re.search(r'directx\s*(\d+(\.\d+)?)', s)
         if m:
            return float(m.group(1))
         return None
      req_dx = extract_dx(required_hw.lower())
      user_dx = None
      # Prefer dxdiag value if available
      if user_hw_dict:
         if user_hw_dict.get('gpu_directx_dxdiag'):
            user_dx = user_hw_dict['gpu_directx_dxdiag']
         elif user_hw_dict.get('gpu_directx'):
            user_dx = user_hw_dict['gpu_directx']
      if user_dx is None:
         user_dx = extract_dx(user_hw_l)
      if req_dx and user_dx:
         if user_dx >= req_dx:
            return True
         else:
            return 'DirectX'
      # VRAM (handle 'dedicated VRAM' phrasing)
      def extract_vram(s):
         # Match 'dedicated' or not, treat both as VRAM requirement
         m = re.search(r'(\d+(\.\d+)?)\s*(gb|mb)\s*(dedicated)?\s*(vram|video|graphics)?', s)
         if m:
            val = float(m.group(1))
            if 'mb' in m.group(0):
               val = val / 1024.0
            return val
         return None
      req_vram = extract_vram(required_hw.lower())
      user_vram = None
      if user_hw_dict and user_hw_dict.get('gpu_vram_gb'):
         user_vram = user_hw_dict['gpu_vram_gb']
      else:
         user_vram = extract_vram(user_hw_l)
      if req_vram and user_vram:
         # For recommended requirements, require user_vram >= req_vram (no +0.1 margin)
         if hw_type == 'gpu' and 'recommended' in (required_hw.lower() if isinstance(required_hw, str) else ''):
            if user_vram >= req_vram:
               return True
            else:
               return 'VRAM'
         # For minimum requirements, allow a small margin
         if user_vram + 0.1 >= req_vram:
            return True
         else:
            return 'VRAM'
      # Modern GPU always sufficient for legacy requirements (broad match, more aggressive)
      legacy_gpu_patterns = [
         r'geforce\s*(8|9|2|3|4|5|6|7|8)\d{2}',
         r'geforce\s*gtx?\s*([1-9]\d{2})',
         r'geforce\s*gt\s*([1-9]\d{2})',
         r'geforce\s*mx',
         r'radeon\s*hd\s*(2|3|4|5|6|7|8)\d{2,4}',
         r'radeon\s*rx?\s*([1-9]\d{2,4})',
         r'radeon\s*vii',
         r'8600', r'9600', r'2600', r'3600', r'610', r'710', r'730', r'5450', r'6450'
      ]
      modern_gpu_keywords = [
         'iris xe', 'iris', 'uhd', 'rtx', 'gtx', 'vega', 'radeon vii', 'rx', 'arc', 'quadro', 'tesla', 'firepro', 'hd graphics', 'mx', 'apple m', 'a100', 'h100', 'p100', 't4', 'v100', 'intel arc', 'intel xe', 'intel hd', 'intel uhd', 'nvidia', 'amd', 'intel'
      ]
      user_gpu_str = ''
      if user_hw_dict and 'gpu' in user_hw_dict:
         user_gpu_str = user_hw_dict['gpu'].lower()
      else:
         user_gpu_str = user_hw_l

      # Pass modern GPUs for generic legacy requirements
      generic_legacy_gpu_phrases = [
         'directx compatible graphics card',
         'directx 7 compatible',
         'directx 8 compatible',
         'directx 9 compatible',
         'directx 10 compatible',
         'directx 11 compatible',
         'hardware t&l',
         '3d accelerator',
         '3d video card',
         'opengl compatible',
         'video card',
         'graphics card',
         'any directx',
         'any 3d',
         'any graphics card',
         'any video card'
      ]
      if any(phrase in req_hw_l for phrase in generic_legacy_gpu_phrases):
         if any(kw in user_gpu_str for kw in modern_gpu_keywords):
            return True
   """
   Robustly compare user hardware to required hardware string.
   - For CPU: compare GHz/MHz, family/brand keywords.
   - For GPU: compare DirectX, VRAM, family/brand keywords.
   - Ignores non-hardware requirements (OS, mouse, etc).
   """
   # Accepts user_hw as string for backward compatibility, but prefers dict with extra fields
   user_hw_dict = None
   if not required_hw or not isinstance(required_hw, str):
      return True
   # If user_hw is a dict (from get_pc_specs), use detailed fields
   if isinstance(user_hw, dict):
      user_hw_dict = user_hw
      user_hw_l = (user_hw.get('cpu_model') or user_hw.get('gpu') or '').lower()
   else:
      user_hw_l = str(user_hw).lower()
   req_hw_l = required_hw.lower()

   # Remove common non-hardware words
   ignore_words = [
      'windows', 'xp', 'vista', '7', '8', '10', '11', 'os x', 'mac', 'linux',
      'mouse', 'keyboard', 'internet', 'connection', 'os:', 'os', 'input', 'sound', 'drive', 'hdd', 'ssd', 'hard drive', 'storage', 'space', 'available', 'free', 'required', 'system', 'requirement', 'network', 'broadband', 'controller', 'directx', 'version', 'service pack', 'sp', 'compatible', 'mb', 'gb', 'ram', 'memory', 'disk', 'api', 'note:', 'see', 'above', 'below', 'etc', 'and', 'or', '(', ')', '[', ']', '{', '}', ',', '.', ';', ':', '®', '&reg;', '®', '™', 'minimum', 'recommended', 'processor:', 'graphics:', 'video:', 'cpu:', 'gpu:'
      # 'geforce', 'radeon', 'ati', 'nvidia', 'amd' intentionally omitted to preserve for matching
   ]
   for word in ignore_words:
      req_hw_l = req_hw_l.replace(word, '')
   req_hw_l = re.sub(r'\s+', ' ', req_hw_l).strip()

   # CPU logic
   if hw_type == 'cpu':
      # Extract GHz/MHz from requirement
      def extract_speed(s):
         m = re.search(r'(\d+(\.\d+)?)\s*(ghz|mhz)', s)
         if m:
            val = float(m.group(1))
            if 'mhz' in m.group(0):
               val = val / 1000.0
            return val
         return None
      req_speed = extract_speed(required_hw.lower())
      user_speed = None
      if user_hw_dict and user_hw_dict.get('cpu_ghz'):
         user_speed = user_hw_dict['cpu_ghz']
      else:
         user_speed = extract_speed(user_hw_l)

      # Modern CPU always sufficient for legacy requirements
      legacy_keywords = ['pentium', 'celeron', 'athlon', 'sempron']
      modern_keywords = ['intel', 'amd', 'core', 'i3', 'i5', 'i7', 'i9', 'ryzen', 'xeon']
      is_legacy_req = any(kw in req_hw_l for kw in legacy_keywords) or (req_speed and req_speed < 3.5)
      is_modern_cpu = False
      cpu_model = ''
      if user_hw_dict and 'cpu_model' in user_hw_dict:
         cpu_model = user_hw_dict['cpu_model'].lower()
      else:
         cpu_model = user_hw_l
      if any(kw in cpu_model for kw in modern_keywords):
         is_modern_cpu = True
      # If GHz is None but model is modern, treat as modern
      if is_legacy_req and is_modern_cpu:
         return True

      if req_speed and user_speed:
         if user_speed + 0.1 >= req_speed:  # allow small margin
            return True
         else:
            return False
      # Check for CPU family/brand keywords
      cpu_keywords = modern_keywords + legacy_keywords
      for kw in cpu_keywords:
         if user_hw_dict and 'cpu_model' in user_hw_dict:
            if kw in user_hw_dict['cpu_model'].lower() and kw in req_hw_l:
               return True
         elif kw in user_hw_l and kw in req_hw_l:
            return True
      # Fallback: substring
      return req_hw_l in user_hw_l

   # GPU logic
   if hw_type == 'gpu':
      # DirectX version
      def extract_dx(s):
         m = re.search(r'directx\s*(\d+(\.\d+)?)', s)
         if m:
            return float(m.group(1))
         return None
      req_dx = extract_dx(required_hw.lower())
      user_dx = None
      # Prefer dxdiag value if available
      if user_hw_dict:
         if user_hw_dict.get('gpu_directx_dxdiag'):
            user_dx = user_hw_dict['gpu_directx_dxdiag']
         elif user_hw_dict.get('gpu_directx'):
            user_dx = user_hw_dict['gpu_directx']
      if user_dx is None:
         user_dx = extract_dx(user_hw_l)
      if req_dx and user_dx:
         if user_dx >= req_dx:
            return True
         else:
            return False
      # VRAM (handle 'dedicated VRAM' phrasing)
      def extract_vram(s):
         # Match 'dedicated' or not, treat both as VRAM requirement
         m = re.search(r'(\d+(\.\d+)?)\s*(gb|mb)\s*(dedicated)?\s*(vram|video|graphics)?', s)
         if m:
            val = float(m.group(1))
            if 'mb' in m.group(0):
               val = val / 1024.0
            return val
         return None
      req_vram = extract_vram(required_hw.lower())
      user_vram = None
      if user_hw_dict and user_hw_dict.get('gpu_vram_gb'):
         user_vram = user_hw_dict['gpu_vram_gb']
      else:
         user_vram = extract_vram(user_hw_l)
      # If requirement mentions 'dedicated' but user VRAM is sufficient, still pass
      if req_vram and user_vram:
         if user_vram + 0.1 >= req_vram:
            return True
         else:
            return False
      # Modern GPU always sufficient for legacy requirements (broad match, more aggressive)
      legacy_gpu_patterns = [
         r'geforce\s*(8|9|2|3|4|5|6|7|8)\d{2}',
         r'geforce\s*gtx?\s*([1-9]\d{2})',
         r'geforce\s*gt\s*([1-9]\d{2})',
         r'geforce\s*mx',
         r'radeon\s*hd\s*(2|3|4|5|6|7|8)\d{2,4}',
         r'radeon\s*rx?\s*([1-9]\d{2,4})',
         r'radeon\s*vii',
         r'8600', r'9600', r'2600', r'3600', r'610', r'710', r'730', r'5450', r'6450'
      ]
      modern_gpu_keywords = [
         'iris xe', 'iris', 'uhd', 'rtx', 'gtx', 'vega', 'radeon vii', 'rx', 'arc', 'quadro', 'tesla', 'firepro', 'hd graphics', 'mx', 'apple m', 'a100', 'h100', 'p100', 't4', 'v100', 'intel arc', 'intel xe', 'intel hd', 'intel uhd', 'nvidia', 'amd', 'intel'
      ]
      user_gpu_str = ''
      if user_hw_dict and 'gpu' in user_hw_dict:
         user_gpu_str = user_hw_dict['gpu'].lower()
      else:
         user_gpu_str = user_hw_l

      # Split requirement string on slashes and commas, check each part for legacy patterns
      legacy_keywords = ['geforce', 'radeon', 'ati', 'amd', 'nvidia']
      req_parts = re.split(r'[\/|,]', req_hw_l)
      legacy_gpu_found = False
      for part in req_parts:
         part = part.strip()
         if any(x in part for x in legacy_keywords):
            legacy_gpu_found = True
            # Dota 2 debug print removed
            # Look for legacy model numbers or patterns
            legacy_model_pattern = r'(\d{4}(?:/\d{4,5})*)|(hd\d{4}(?:/\d{4,5})*)|(\d{4,5}gt)|(hd\d{4,5})|((geforce|radeon|ati|amd)[^\d]*\d{4}(?:/\d{4,5})*)|((geforce|radeon|ati|amd)[^\d]*hd\d{4}(?:/hd\d{4,5})*)'
            if re.search(legacy_model_pattern, part):
               if any(kw in user_gpu_str for kw in modern_gpu_keywords):
                  # Dota 2 debug print removed
                  return True
            # Also check legacy patterns
            for pat in legacy_gpu_patterns:
               if re.search(pat, part):
                  if any(kw in user_gpu_str for kw in modern_gpu_keywords):
                     # Dota 2 debug print removed
                     return True
            # If requirement mentions 'geforce', 'radeon', 'ati', 'amd', or 'nvidia' and user GPU is modern, always pass (fallback)
            if any(kw in user_gpu_str for kw in modern_gpu_keywords):
               # Dota 2 debug print removed
               return True
      # If all GPU requirements are legacy (NVIDIA/ATI/AMD) and user GPU is modern (including Intel), always pass
      if legacy_gpu_found and all(any(x in part for x in legacy_keywords) for part in req_parts):
         # Dota 2 debug print removed
         if any(kw in user_gpu_str for kw in modern_gpu_keywords):
            # Dota 2 debug print removed
            return True
      # If all GPU requirements are legacy (NVIDIA/ATI/AMD) and user GPU is modern (including Intel), always pass
      if legacy_gpu_found and all(any(x in part for x in legacy_keywords) for part in req_parts):
         if any(kw in user_gpu_str for kw in modern_gpu_keywords):
            return True
      # Otherwise, fallback to keyword matching
      gpu_keywords = ['intel', 'nvidia', 'amd', 'radeon', 'geforce', 'quadro', 'rtx', 'gtx', 'vega', 'iris', 'hd graphics']
      for kw in gpu_keywords:
         if user_hw_dict and 'gpu' in user_hw_dict:
            if kw in user_hw_dict['gpu'].lower() and kw in req_hw_l:
               return True
         elif kw in user_hw_l and kw in req_hw_l:
            return True
      # Fallback: substring
      if req_hw_l not in user_hw_l:
         return 'Model'
      return True

   # Default fallback: substring
   return req_hw_l in user_hw_l
def resolve_steamid(api_key, user_input):
   """
   Resolves a SteamID64 from a username or returns the input if it's already a 17-digit SteamID64.
   """
   user_input = user_input.strip()
   if user_input.isdigit() and len(user_input) == 17:
      return user_input
   # Try to resolve custom URL name
   url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={api_key}&vanityurl={user_input}"
   try:
      resp = requests.get(url, timeout=10)
      data = resp.json()
      if data.get('response', {}).get('success') == 1:
         return data['response']['steamid']
      else:
         print(f"Could not resolve username '{user_input}' to a SteamID64. Please check the username or use your 17-digit SteamID.")
         return None
   except Exception as e:
      print(f"Error resolving Steam username: {e}")
      return None



import sys
import subprocess


# Auto-install required packages if missing

# Improved package check: only print 'Installing...' if not present in current environment
required = ["psutil", "GPUtil", "requests", "wmi"]
import importlib.util
missing_pkgs = []
for pkg in required:
   already_imported = False
   if pkg == "GPUtil":
      spec = importlib.util.find_spec("GPUtil")
      already_imported = spec is not None
   else:
      try:
         __import__(pkg)
         already_imported = True
      except ImportError:
         already_imported = False
   if not already_imported:
      missing_pkgs.append(pkg)

if missing_pkgs:
   print("The following required packages are missing:")
   for pkg in missing_pkgs:
      print(f"  - {pkg}")
   approve = input("Do you want to install the missing packages now? [Y/n]: ").strip().lower()
   if approve in ("", "y", "yes"):
      for pkg in missing_pkgs:
         print(f"Installing {pkg}...")
         try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
         except Exception as e:
            print(f"Failed to install {pkg}: {e}")
   else:
      print("Cannot continue without required packages. Exiting.")
      sys.exit(1)

import platform
import psutil
import requests
import time
import threading
import re
from difflib import SequenceMatcher
try:
   import GPUtil
except ImportError:
   GPUtil = None


def get_pc_specs():
   # Try to get DirectX version using dxdiag
   import subprocess
   import os
   dxdiag_version = None
   dxdiag_feature_levels = None
   dxdiag_shader_model = None
   try:
      dxdiag_path = 'dxdiag.txt'
      subprocess.run(['dxdiag', '/t', dxdiag_path], check=True, timeout=60)
      with open(dxdiag_path, 'r', encoding='utf-8', errors='ignore') as f:
         dxdiag_text = f.read()
      # Try multiple patterns for DirectX Version
      m_ver = (
         re.search(r'DirectX Version\s*[:\-]?\s*(?:DirectX\s*)?(\d+(?:\.\d+)?)', dxdiag_text, re.IGNORECASE)
         or re.search(r'DirectX-Version\s*[:\-]?\s*(?:DirectX\s*)?(\d+(?:\.\d+)?)', dxdiag_text, re.IGNORECASE)
         or re.search(r'DirectX\s*Version\s*[:\-]?\s*(\d+(?:\.\d+)?)', dxdiag_text, re.IGNORECASE)
         or re.search(r'DirectX\s*:\s*(\d+(?:\.\d+)?)', dxdiag_text, re.IGNORECASE)
      )
      if m_ver:
         try:
            dxdiag_version = float(m_ver.group(1))
         except Exception:
            dxdiag_version = None
      # Try multiple patterns for Feature Levels
      m_feat = (
         re.search(r'Feature Levels?\s*[:\-]?\s*([\d_.,;\s]+)', dxdiag_text.replace('\r', '').replace('\n', ' '), re.IGNORECASE)
         or re.search(r'Feature Level\s*[:\-]?\s*([\d_.,;\s]+)', dxdiag_text.replace('\r', '').replace('\n', ' '), re.IGNORECASE)
      )
      if m_feat:
         fls = m_feat.group(1)
         dxdiag_feature_levels = [fl.strip() for fl in re.split(r',|;', fls) if fl.strip()]
      # If neither found, print first 40 lines for debugging
      if dxdiag_version is None or dxdiag_feature_levels is None:
         print("\n[Debug] Could not find DirectX Version or Feature Levels in dxdiag.txt. First 40 lines:")
         with open(dxdiag_path, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
               if i >= 40:
                  break
               print(line.rstrip())
      # Clean up
      try:
         os.remove(dxdiag_path)
      except Exception:
         pass
   except Exception as e:
      print(f"[Debug] Exception running dxdiag: {e}")
   # Map feature level to Shader Model
   featurelevel_to_shader_model = {
      '12_2': '6.6',
      '12_1': '6.5',
      '12_0': '6.0',
      '11_1': '5.1',
      '11_0': '5.0',
      '10_1': '4.1',
      '10_0': '4.0',
      '9_3': '3.0',
      '9_2': '2.0',
      '9_1': '2.0',
   }
   if dxdiag_feature_levels:
      # Pick the highest feature level
      for fl in dxdiag_feature_levels:
         if fl in featurelevel_to_shader_model:
            dxdiag_shader_model = featurelevel_to_shader_model[fl]
            break
   specs = {}
   # Group all GPU info together
   gpu_name = None
   gpu_vram_gb = None
   if GPUtil:
      try:
         gpus = GPUtil.getGPUs()
         if gpus:
            gpu = gpus[0]
            gpu_name = gpu.name
            if hasattr(gpu, 'memoryTotal'):
               gpu_vram_gb = round(float(gpu.memoryTotal), 2)
      except Exception:
         pass
   try:
      import wmi
      w = wmi.WMI()
      gpus = w.Win32_VideoController()
      if gpus:
         gpu = gpus[0]
         if not gpu_name:
            gpu_name = getattr(gpu, 'Name', None)
         vram = getattr(gpu, 'AdapterRAM', None)
         if vram:
            gpu_vram_gb = round(float(vram) / (1024 ** 3), 2)
   except Exception:
      pass
   specs['gpu'] = gpu_name or 'No GPU detected (Intel/AMD/NVIDIA)'
   specs['gpu_vram_gb'] = gpu_vram_gb
   specs['gpu_directx_dxdiag'] = dxdiag_version
   specs['gpu_feature_levels'] = dxdiag_feature_levels
   specs['gpu_shader_model'] = dxdiag_shader_model
   # CPU and RAM info
   import platform
   specs['cpu'] = platform.processor() or platform.uname().processor or platform.uname().machine
   import math
   specs['ram_gb'] = math.ceil(psutil.virtual_memory().total / (1024 ** 3))
   specs['disk_gb'] = round(psutil.disk_usage('/') .free / (1024 ** 3), 2)
   try:
      import wmi
      w = wmi.WMI()
      cpus = w.Win32_Processor()
      if cpus:
         cpu = cpus[0]
         specs['cpu_model'] = getattr(cpu, 'Name', specs['cpu'])
         max_clock = getattr(cpu, 'MaxClockSpeed', None)
         if max_clock:
            specs['cpu_ghz'] = round(float(max_clock) / 1000.0, 2)
         else:
            m = re.search(r'(\d+\.?\d*)\s*GHz', specs['cpu_model'])
            if m:
               specs['cpu_ghz'] = float(m.group(1))
   except Exception:
      specs['cpu_model'] = specs['cpu']
      specs['cpu_ghz'] = None
   return specs

"""
Steam Library Specs Checker

This script will help you find which games in your Steam library your current PC can run.

Step 1: Get your Steam User ID
--------------------------------
1. Go to https://store.steampowered.com/login/ and log in to your Steam account.
2. Click on your profile name at the top, then click 'View my profile'.
3. Your Steam ID is the long number in the URL (e.g., https://steamcommunity.com/profiles/12345678901234567).
   - If you see a custom name instead, click 'Edit Profile' and look for your Steam ID number.

Step 2: Make your profile public (if needed)
---------------------------------------------
1. On your profile page, click 'Edit Profile'.
2. Go to 'Privacy Settings'.
3. Set 'My Profile' and 'Game details' to 'Public'.

This is required for the script to access your game library via the Steam Web API.

Continue running this script to proceed with checking your PC specs against your Steam library.
"""


import requests
import sys

def get_steam_library(api_key, steam_id):
   """
   Fetches the user's Steam library using the Steam Web API.
   Returns a list of game appids and names, or None if the profile is private or invalid.
   """
   url = (
      f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={api_key}&steamid={steam_id}&include_appinfo=1&include_played_free_games=1"
   )
   try:
      response = requests.get(url, timeout=10)
      if response.status_code != 200:
         print("Error: Could not reach Steam API.")
         return None
      data = response.json()
      if 'response' not in data or 'games' not in data['response']:
         print("No games found. Your profile may be private or the Steam ID/API key is incorrect.")
         print("Make sure your profile and game details are set to public in Steam privacy settings.")
         return None
      return data['response']['games']
   except Exception as e:
      print(f"Error fetching Steam library: {e}")
      return None

#########################
# API Rate Limiting & Caching
#########################
# Steam recommends ~200 requests per 5 minutes (1 request every 1.5s is safe)
API_RATE_LIMIT = 200
API_RATE_PERIOD = 300  # seconds (5 minutes)
API_MIN_INTERVAL = API_RATE_PERIOD / API_RATE_LIMIT  # 1.5s

# Simple in-memory cache for appdetails

import json
appdetails_cache = {}
appdetails_cache_path = 'appdetails_cache.json'
# Load cache from file if it exists
try:
   with open(appdetails_cache_path, 'r', encoding='utf-8') as f:
      appdetails_cache = json.load(f)
except Exception:
   appdetails_cache = {}

# Thread-safe last request time
_last_api_call = [0]
_api_lock = threading.Lock()

def rate_limited_request(url, cache_key=None, use_cache=True):
   # Use cache if available
   if use_cache and cache_key and str(cache_key) in appdetails_cache:
      # Return a mock response object with .status_code and .json()
      class CachedResp:
         def __init__(self, data):
            self._data = data
            self.status_code = 200
         def json(self):
            return self._data
      return CachedResp(appdetails_cache[str(cache_key)])
   # Rate limit
   with _api_lock:
      now = time.time()
      elapsed = now - _last_api_call[0]
      if elapsed < API_MIN_INTERVAL:
         time.sleep(API_MIN_INTERVAL - elapsed)
      _last_api_call[0] = time.time()
   resp = requests.get(url, timeout=10)
   if cache_key is not None and resp.status_code == 200:
      try:
         # Load the full cache from disk to avoid overwriting
         try:
            with open(appdetails_cache_path, 'r', encoding='utf-8') as f:
               disk_cache = json.load(f)
         except Exception:
            disk_cache = {}
         # Extract only title, requirements, and score
         data = resp.json()
         entry = {}
         def strip_html(text):
            if not text:
               return ''
            # Remove HTML tags and excess whitespace
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            return text.strip()
         if data and str(cache_key) in data and data[str(cache_key)].get('success'):
            game_data = data[str(cache_key)]['data']
            entry['title'] = game_data.get('name')
            if 'pc_requirements' in game_data:
               pc_reqs = game_data['pc_requirements']
               # Strip HTML from minimum and recommended
               clean_reqs = {}
               for k in ('minimum', 'recommended'):
                  if k in pc_reqs and pc_reqs[k]:
                     clean_reqs[k] = strip_html(pc_reqs[k])
               entry['pc_requirements'] = clean_reqs
            # Save score if present (Steam API: 'metacritic' or 'score' field)
            score = None
            if 'metacritic' in game_data and isinstance(game_data['metacritic'], dict):
               score = game_data['metacritic'].get('score')
            elif 'score' in game_data:
               score = game_data['score']
            if score is not None:
               entry['score'] = score
         disk_cache[str(cache_key)] = entry
         appdetails_cache.update(disk_cache)
         # Write the updated cache back to disk
         with open(appdetails_cache_path, 'w', encoding='utf-8') as f:
            json.dump(disk_cache, f, indent=2)
      except Exception:
         pass
   return resp
def fetch_game_requirements(appid):
   """
   Fetches minimum and recommended system requirements for a game from the Steam Store API.
   Returns a dict with 'minimum' and 'recommended' keys (HTML text), or None if not found.
   Uses in-memory cache and rate limiting.
   """
   url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us&l=en"
   from_cache = False
   # Check if in cache before calling
   if str(appid) in appdetails_cache:
      from_cache = True
   try:
      resp = rate_limited_request(url, cache_key=appid)
      if resp.status_code != 200:
         return None, from_cache, resp.status_code
      data = resp.json()
      if not data or not data.get(str(appid), {}).get('success'):
         return None, from_cache, None
      game_data = data[str(appid)]['data']
      if 'pc_requirements' in game_data:
         pc_reqs = game_data['pc_requirements']
         # If recommended is missing but minimum contains both, split them
         if (
            'minimum' in pc_reqs and
            (not pc_reqs.get('recommended')) and
            ('Recommended:' in pc_reqs['minimum'] or 'RECOMMENDED:' in pc_reqs['minimum'])
         ):
            min_html = pc_reqs['minimum']
            # Try to split at Recommended: (case-insensitive)
            split = re.split(r'<strong>Recommended:</strong>|<b>Recommended:</b>|Recommended:', min_html, flags=re.IGNORECASE)
            if len(split) == 2:
               pc_reqs['minimum'] = split[0].strip()
               pc_reqs['recommended'] = split[1].strip()
         # If neither minimum nor recommended exists, but a generic 'requirements' field exists, treat as recommended
         if (
            'minimum' not in pc_reqs and
            'recommended' not in pc_reqs and
            'requirements' in pc_reqs and pc_reqs['requirements']
         ):
            pc_reqs['recommended'] = pc_reqs['requirements']
         return pc_reqs, from_cache, None
      return None, from_cache, None
   except Exception as e:
      # Check for timeout
      import socket
      if isinstance(e, (socket.timeout, TimeoutError)) or 'timed out' in str(e).lower():
         return None, from_cache, 'timeout'
      return None, from_cache, 'error'


def parse_requirements(requirements_html):
   """
   Parses the requirements HTML to extract CPU, GPU, RAM, and disk space as strings.
   Returns a dict with those fields if found. Logs raw requirements if parsing fails.
   """
   if not requirements_html:
      return {}
   reqs = {}
   # Remove HTML tags and normalize whitespace
   text = re.sub(r'<[^>]+>', '\n', requirements_html)
   text = re.sub(r'\n+', '\n', text)
   # Special case: detect "Requires a 64-bit processor and operating system"
   if re.search(r'requires a 64-bit processor and operating system', text, re.IGNORECASE):
      reqs['os'] = '64-bit processor and operating system'
   # Split on known field delimiters
   # Example: "Processor: ... Memory: ... Graphics: ... Storage: ..."
   field_map = {
      'cpu': ['processor', 'cpu'],
      'gpu': ['graphics', 'gpu', 'video card', 'video'],
      'ram': ['memory', 'ram'],
      'disk': ['storage', 'hard drive', 'disk']
   }
   # Build regex pattern to split on all known fields
   split_pattern = r'(Processor:|CPU:|Graphics:|GPU:|Video Card:|Video:|Memory:|RAM:|Storage:|Hard Drive:|Disk:|DirectX:|Sound Card:|Network:|OS:|Operating System:|Minimum:|Recommended:|\n)'
   segments = re.split(split_pattern, text, flags=re.IGNORECASE)
   # Merge field names with their values
   pairs = []
   i = 0
   while i < len(segments) - 1:
      seg = segments[i].strip()
      val = segments[i+1].strip()
      if seg.endswith(':'):
         pairs.append((seg[:-1].lower(), val))
         i += 2
      else:
         i += 1
   # Assign to reqs dict
   for field, keys in field_map.items():
      for k, v in pairs:
         if any(key in k for key in keys):
            reqs[field] = v
            break
   # Fallback: try to find first numbers with GB/MB if not found
   if 'ram' not in reqs:
      m = re.search(r'(\d+\.?\d*)\s*(GB|MB)\s*(RAM|Memory)?', text, re.IGNORECASE)
      if m:
         reqs['ram'] = m.group(0)
   if 'disk' not in reqs:
      m = re.search(r'(\d+\.?\d*)\s*(GB|MB)\s*(Storage|Disk|Hard Drive)?', text, re.IGNORECASE)
      if m:
         reqs['disk'] = m.group(0)
   # If nothing found, log the raw requirements for review
   if not reqs:
      with open('unparsed_requirements.log', 'a', encoding='utf-8') as f:
         f.write('---\n')
         f.write(text.strip() + '\n')
   return reqs
if __name__ == "__main__":
   try:
      print("\n--- Steam Library Specs Checker ---\n")
      import os
      user_details_path = 'user_details.json'
      user_details = {"api_key": None, "steam_id": None, "user_input": None, "username": None}
      # Try to load user details if they exist
      if os.path.exists(user_details_path):
         try:
            with open(user_details_path, 'r', encoding='utf-8') as f:
               user_details = json.load(f)
         except Exception:
            pass
      # Prompt for API key if not cached
      api_key = user_details.get("api_key")
      if not api_key:
         api_key = input("Enter your Steam Web API key: ").strip()
         while not api_key:
            print("API key is required.")
            api_key = input("Enter your Steam Web API key: ").strip()
      # Prompt for user input if not cached
      user_input = user_details.get("user_input")
      steam_id = user_details.get("steam_id")
      if not user_input or not steam_id:
         user_input = input("Enter your Steam ID (17-digit number) or custom profile name: ").strip()
         while not user_input:
            print("Steam ID or profile name is required.")
            user_input = input("Enter your Steam ID (17-digit number) or custom profile name: ").strip()
         steam_id = resolve_steamid(api_key, user_input)
         username = user_input if not user_input.isdigit() else None
         user_details = {"api_key": api_key, "steam_id": steam_id, "user_input": user_input, "username": username}
         # Save details for next time
         try:
            with open(user_details_path, 'w', encoding='utf-8') as f:
               json.dump(user_details, f, indent=2)
         except Exception:
            pass
      else:
         username = user_details.get("username")
      if not steam_id:
         sys.exit(1)
      games = get_steam_library(api_key, steam_id)
      if not games:
         sys.exit(1)
      print(f"\nFound {len(games)} games in your Steam library.")
      limit_games = input("Process only the first 10 games? (y/N): ").strip().lower() == 'y'
      if limit_games:
         games = games[:10]
         print("Processing only the first 10 games...")
      # Gather PC specs (use cache if available)
      print("\nGathering your PC specs...")
      pc_specs_path = 'pc_specs.json'
      specs = None
      import json
      try:
         if os.path.exists(pc_specs_path):
            with open(pc_specs_path, 'r', encoding='utf-8') as f:
               specs = json.load(f)
         # Validate minimal required fields in cache
         if not specs or not isinstance(specs, dict) or not specs.get('cpu_model') or not specs.get('gpu'):
            specs = get_pc_specs()
            # Update cache
            try:
               with open(pc_specs_path, 'w', encoding='utf-8') as f:
                  json.dump(specs, f, indent=2)
            except Exception as e:
               print(f"[Warning] Could not write PC specs to {pc_specs_path}: {e}")
      except Exception as e:
         print(f"Error loading PC specs from cache: {e}")
         specs = get_pc_specs()
         try:
            with open(pc_specs_path, 'w', encoding='utf-8') as f:
               json.dump(specs, f, indent=2)
         except Exception as e2:
            print(f"[Warning] Could not write PC specs to {pc_specs_path}: {e2}")

      # Print API/user details in a separate section
      def mask_key(key):
         if not key or len(key) < 8:
            return key
         return key[:4] + "..." + key[-4:]
      print("\nUser/API Details:")
      print(f"  API Key: {mask_key(api_key)}")
      print(f"  Steam ID: {steam_id}")
      print(f"  Username: {user_input}")
      print("\nDetected PC Specs:")
      # Tidy GPU info
      print("  GPU:")
      print(f"    Name: {specs.get('gpu')}")
      if specs.get('gpu_vram_gb') is not None:
         print(f"    VRAM (GB): {specs.get('gpu_vram_gb')}")
      if specs.get('gpu_directx_dxdiag') is not None:
         print(f"    DirectX Version: {specs.get('gpu_directx_dxdiag')}")
      if specs.get('gpu_feature_levels'):
         print(f"    Feature Levels: {', '.join(str(x) for x in specs['gpu_feature_levels'])}")
      if specs.get('gpu_shader_model'):
         print(f"    Shader Model: {specs['gpu_shader_model']} (from Feature Level)")
      else:
         print("    Shader Model: [Could not determine from dxdiag]")

      # Tidy CPU info
      print("  CPU:")
      print(f"    Model: {specs.get('cpu_model')}")
      if specs.get('cpu_ghz') is not None:
         print(f"    Max Clock (GHz): {specs.get('cpu_ghz')}")

      # RAM and Disk
      print(f"  RAM (GB): {specs.get('ram_gb')}")
      print(f"  Free Disk Space (GB): {specs.get('disk_gb')}")
      # Fetch and compare game requirements
      print("\nChecking your games against your PC specs (this may take a few minutes)...")
      # Prepare for aligned output: determine max title/score widths for the games being processed
      max_title = 0
      max_score = 0
      max_display_title = 40  # Truncate game names to this length for display
      game_rows = []
      for game in games:
         appid = game['appid']
         name = game.get('name', f"AppID {appid}")
         display_name = name
         if len(display_name) > max_display_title:
            display_name = display_name[:max_display_title-3] + '...'
         cache_entry = appdetails_cache.get(str(appid))
         score = None
         if cache_entry and 'score' in cache_entry:
            score = cache_entry['score']
         score_str = str(score) if score is not None else "-"
         max_title = max(max_title, len(display_name))
         max_score = max(max_score, len(score_str))
         game_rows.append((appid, name, display_name, score_str))

      min_title = max(24, min(max_display_title, max_title))
      min_score = max(5, max_score)
      status_width = 9
      note_width = 8
      unmet_width = 10
      # Print header with new 'Unmet' column
      print(f"{'Title':<{min_title}} {'Score':>{min_score}} {'Status':<{status_width}} {'Note':<{note_width}} {'Unmet':<{unmet_width}}")
      print(f"{'-'*min_title} {'-'*min_score} {'-'*status_width} {'-'*note_width} {'-'*unmet_width}")

      # Second pass: process and print each game immediately
      for idx, game in enumerate(games):
         appid, name, display_name, score_str = game_rows[idx]
         appid = game['appid']
         name = game.get('name', f"AppID {appid}")
         # Always truncate display_name for alignment
         display_name = name
         if len(display_name) > max_display_title:
            display_name = display_name[:max_display_title-3] + '...'
         reqs, from_cache, reqs_error = fetch_game_requirements(appid)
         # Get score from cache if available
         score = None
         cache_entry = appdetails_cache.get(str(appid))
         if cache_entry and 'score' in cache_entry:
            score = cache_entry['score']
         score_str = str(score) if score is not None else "-"
         only_recommended = reqs and not reqs.get('minimum') and reqs.get('recommended')
         cache_note = "[CACHED]" if from_cache else "[LIVE]"

         status = ""
         reason = ""
         # Fix: If requirements are missing but cache entry has pc_requirements, use them
         if (not reqs or not isinstance(reqs, dict) or not reqs.get('minimum')) and from_cache:
            cache_entry = appdetails_cache.get(str(appid))
            if cache_entry and 'pc_requirements' in cache_entry:
               reqs = cache_entry['pc_requirements']
         # Parse requirements and check
         if only_recommended:
            min_reqs = parse_requirements(reqs['recommended'])
            rec_reqs = min_reqs
         else:
            if not reqs or not reqs.get('minimum'):
               if reqs_error == 'timeout':
                  status = "timeout"
                  note = "timeout"
               else:
                  status = "unlisted"
                  note = "unlisted"
               unmet = "-"
               print(f"{display_name:<{min_title}} {score_str:>{min_score}} {status:<{status_width}} {note:<{note_width}} {unmet:<{unmet_width}}")
               time.sleep(0.5)
               continue
            min_reqs = parse_requirements(reqs['minimum'])
            rec_reqs = parse_requirements(reqs.get('recommended')) if reqs.get('recommended') else None
            # Dota 2 debug print removed
            if not isinstance(min_reqs, dict) or not min_reqs:
               status = "PARSE?"
               note = "unlisted"
               unmet = "-"
               print(f"{name:<{min_title}} {score_str:>{min_score}} {status:<{status_width}} {note:<{note_width}} {unmet:<{unmet_width}}")
               time.sleep(0.5)
               continue

         def check_reqs(reqs_dict):
            meets = True
            reasons = []
            # RAM check
            if 'ram' in reqs_dict:
               ram_match = re.search(r'(\d+(\.\d+)?)\s*GB', reqs_dict['ram'], re.IGNORECASE)
               if ram_match:
                  required_ram = float(ram_match.group(1))
                  if specs['ram_gb'] < required_ram:
                     meets = False
                     reasons.append("RAM")
            # Disk check
            if 'disk' in reqs_dict:
               disk_match = re.search(r'(\d+(\.\d+)?)\s*GB', reqs_dict['disk'], re.IGNORECASE)
               if disk_match:
                  required_disk = float(disk_match.group(1))
                  if specs['disk_gb'] < required_disk:
                     meets = False
                     reasons.append("DISK")
            # CPU check
            if 'cpu' in reqs_dict:
               cpu_result = is_cpu_gpu_sufficient(specs, reqs_dict['cpu'], hw_type='cpu')
               if cpu_result is not True:
                  meets = False
                  # Only show reason, not details
                  if isinstance(cpu_result, str) and cpu_result not in ("True", "False"):
                     # Try to extract a reason keyword from the string
                     if 'ghz' in cpu_result.lower():
                        reasons.append("CPU")
                     elif 'model' in cpu_result.lower():
                        reasons.append("CPU")
                     else:
                        reasons.append("CPU")
                  else:
                     reasons.append("CPU")
            # GPU check
            if 'gpu' in reqs_dict:
               gpu_result = is_cpu_gpu_sufficient(specs, reqs_dict['gpu'], hw_type='gpu')
               if gpu_result is not True:
                  meets = False
                  # Only show reason, not details
                  if isinstance(gpu_result, str) and gpu_result not in ("True", "False"):
                     # Use only the main reason (e.g., VRAM, DirectX, Model)
                     main_reason = str(gpu_result).split('(')[0].split('<')[0].strip()
                     reasons.append(main_reason)
                  else:
                     reasons.append("GPU")
            return meets, reasons

         meets_rec, reasons_rec = check_reqs(rec_reqs) if rec_reqs else (False, ["No recommended"])
         meets_min, reasons_min = check_reqs(min_reqs)

         # Determine unmet requirements for display
         unmet = "-"
         if only_recommended:
            if meets_rec:
               status = "REC"
               unmet = "-"
            else:
               status = "NO"
               unmet = ','.join(reasons_rec) if reasons_rec else "-"
         else:
            # If there is no recommended requirements, treat meeting minimum as REC
            if not rec_reqs or (reasons_rec and reasons_rec[0] == "No recommended"):
               if meets_min:
                  status = "REC"
                  unmet = "-"
               else:
                  status = "NO"
                  unmet = ','.join(reasons_min) if reasons_min else "-"
            elif meets_rec:
               status = "REC"
               unmet = "-"
            elif meets_min:
               status = "MIN"
               unmet = ','.join(reasons_rec) if reasons_rec else "-"
            else:
               status = "NO"
               unmet = ','.join(reasons_min) if reasons_min else "-"
         print(f"{display_name:<{min_title}} {score_str:>{min_score}} {status:<{status_width}} {cache_note:<{note_width}} {unmet:<{unmet_width}}")
         time.sleep(0.5)  # Be polite to Steam API
   except KeyboardInterrupt:
      print("\nScript interrupted by user. Exiting cleanly.")
      sys.exit(0)
