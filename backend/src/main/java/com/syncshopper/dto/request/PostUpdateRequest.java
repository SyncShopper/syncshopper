package com.syncshopper.dto.request;

import com.syncshopper.domain.post.PostType;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class PostUpdateRequest {

    @NotBlank(message = "Title is required")
    @Schema(description = "Post title", example = "Updated System Maintenance Notice")
    private String title;

    @NotBlank(message = "Content is required")
    @Schema(description = "Post content", example = "System maintenance is complete.")
    private String content;

    @NotNull(message = "Post type is required")
    @Schema(description = "Post type (NOTICE, FAQ, EVENT)", example = "NOTICE")
    private PostType postType;

    @NotBlank(message = "Visibility flag is required")
    @Schema(description = "Visible flag (Y/N)", example = "Y")
    private String visibleYn;
}
